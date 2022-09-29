import pickle
import time
from typing import Optional
import typer
from rich.progress import track

from .fotoparadies import FotoparadiesStatus
from rich.console import Console
from rich.table import Table
from platformdirs import user_config_dir
from pathlib import Path

app = typer.Typer()
console = Console()


def _get_orders_filepath() -> Path:
    """Gibt einen Pfad zurück, an dem die Aufträge als Pickle-Datei abgelegt werden können.
    Der Pfad ist abhängig vom Betriebssystem. Der Pfad wird angelegt, falls er nicht existiert.

    Returns:
        Path: Der Pfad, an dem die Aufträge als Pickle exportiert werden können.
    """
    app_path = Path(user_config_dir(appname="fotoparadies-status", appauthor="hija"))
    app_path.mkdir(parents=True, exist_ok=True)

    order_file = app_path / "orders.pkl"
    return order_file


def get_orders_list() -> list[FotoparadiesStatus]:
    """Liest die eingespeicherte Pickle Datei ein und gibt eine Liste mit Auftragsstati zurück.

    Returns:
        list[FotoparadiesStatus]: Liste mit Fotoparadies-Stati
    """
    order_file = _get_orders_filepath()
    if order_file.exists():
        file = open(order_file, "rb")
        return pickle.load(file)

    return []


def save_orders_list(list: list[FotoparadiesStatus]):
    """Speichert die Auftragsstati in einer Pickledatei ab

    Args:
        list (list[FotoparadiesStatus]): Liste der Autragsstati, die abgespeichert werden sollen.
    """
    order_file = _get_orders_filepath()
    pickle.dump(list, open(order_file, "wb"))


def _print_table_with_status(fp_stati: list[FotoparadiesStatus]):
    """Gibt eine ASCII-Tabelle mit den Auftragsstati aus.

    Args:
        fp_stati (list[FotoparadiesStatus]): Die Auftragsstati, die ausgegeben werden sollen.
    """

    table = Table("Name", "Letztes Update", "Status", "Preis")

    for fp_status in fp_stati:
        table.add_row(
            fp_status.ordername,
            fp_status.getlastupdate,
            fp_status.currentstatus,
            fp_status.price,
        )

    console.print(table)


@app.command()
def status():
    """Gibt die Stati der abgespeicherten Aufträge in einer Tabelle aus"""
    current_list = get_orders_list()

    for fp_status in track(
        current_list,
        description="Aufträge werden aktualisiert",
        total=len(current_list),
    ):
        fp_status.refresh()
        time.sleep(
            1
        )  # Nach jeder Aktualisierung wird 1s gewartet um die API nicht zu überfordern

    save_orders_list(current_list)
    _print_table_with_status(current_list)


@app.command()
def add(shop: int, order: int, name: Optional[str] = typer.Argument(None)):
    """Fügt einen Fotoauftrag hinzu

    Args:
        shop (int): Der DM Store, an dem der Auftrag abgegeben wurde
        order (int): Die Auftragsnummer
        name (Optional[str], optional): Ein Name, mit dem der Auftrag wiedererkannt werden kann
    """
    fp_status = FotoparadiesStatus(shop, order, name, fetch_data=False)
    current_list = get_orders_list()

    for elem in current_list:
        if elem._order == order and elem._shop == shop:
            console.print(
                f":x: Der Auftrag [bold]befindet sich bereits[/bold] unter dem Name {elem.ordername} [bold]in der Liste[/bold]!"
            )
            return
        if elem.ordername == name:
            console.print(
                ":x: Ein Auftrag mit identischem Namen befindet sich bereits in der Liste. Ein weiterer [bold]Auftrag muss[/bold] einen [bold]anderen Namen haben[/bold]."
            )

    current_list.append(fp_status)
    save_orders_list(current_list)
    console.print(
        ":heavy_check_mark: Der [bold]Auftrag[/bold] wurde [bold]hinzugefügt[/bold]."
    )


@app.command()
def remove(name: str):
    """Löscht einen Fotoauftrag

    Args:
        name (str): Der Name des Auftrags
    """
    current_list = get_orders_list()
    for elem in current_list:
        if elem.ordername and elem.ordername == name:
            current_list.remove(elem)
            console.print(":heavy_check_mark: Der [bold]Auftrag wurde gelöscht[/bold]!")
            save_orders_list(current_list)
            return
    console.print(":x: Der [bold]Auftrag[/bold] wurde [bold]nicht gefunden[/bold].")


@app.command()
def cleanup():
    """Löscht Aufträge, die bereits zurückgeschickt wurden (Status DELIVERED)"""

    current_list = get_orders_list()
    list_without_delivered = [
        order
        for order in current_list
        if not (order.currentstatus and order.currentstatus == "DELIVERED")
    ]
    save_orders_list(list_without_delivered)

    removed_entries = len(current_list) - len(list_without_delivered)
    if removed_entries > 0:
        console.print(
            f":heavy_check_mark: Es [bold]wurde(n) {removed_entries} Aufträge[/bold], die bereits geliefert wurden, [bold]gelöscht[/bold]."
        )
    else:
        console.print(
            ":x: Es [bold]gab keinen Auftrag[/bold], der gelöscht werden konnte."
        )


if __name__ == "__main__":
    app()
