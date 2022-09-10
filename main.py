import pickle
from typing import Optional
import typer

from fotoparadies import FotoparadiesStatus
from rich.console import Console
from rich.table import Table
from platformdirs import user_config_dir
from pathlib import Path

app = typer.Typer()
console = Console()


def _get_orders_filepath() -> Path:
    app_path = Path(user_config_dir(appname="fotoparadies-status", appauthor="hija"))
    app_path.mkdir(parents=True, exist_ok=True)

    order_file = app_path / "orders.pkl"
    return order_file


def get_orders_list() -> list[FotoparadiesStatus]:
    order_file = _get_orders_filepath()
    if order_file.exists():
        file = open(order_file, "rb")
        return pickle.load(file)

    return []


def save_orders_list(list: list[FotoparadiesStatus]):
    order_file = _get_orders_filepath()
    pickle.dump(list, open(order_file, "wb"))


def _print_table_with_status(fp_stati: list[FotoparadiesStatus]):

    table = Table("Name", "Letztes Update", "Status", "Preis")

    for fp_status in fp_stati:
        table.add_row(
            fp_status.ordername,
            fp_status.getlastupdate,
            fp_status.currentstatus,
            str(fp_status.price),
        )

    console.print(table)


@app.command()
def status():
    current_list = get_orders_list()
    ### TODO: SLIDER
    for fp_status in current_list:
        fp_status.refresh()

    save_orders_list(current_list)
    _print_table_with_status(current_list)


@app.command()
def add(shop: int, order: int, name: Optional[str] = typer.Argument(None)):
    fp_status = FotoparadiesStatus(shop, order, name, fetch_data=False)
    current_list = get_orders_list()

    for elem in current_list:
        if elem._order == order and elem._shop == shop:
            console.print(
                f"Der Auftrag befindet sich bereits unter dem Name {elem.ordername} in der Liste!"
            )
            return
        if elem.ordername == name:
            console.print(
                "Ein Auftrag mit identischem Namen befindet sich bereits in der Liste. Ein weiterer Auftrag muss einen anderen Namen haben."
            )

    current_list.append(fp_status)
    save_orders_list(current_list)
    console.print("Der Auftrag wurde hinzugefügt.")


@app.command()
def remove(name: str):
    current_list = get_orders_list()
    for elem in current_list:
        if elem.ordername and elem.ordername == name:
            current_list.remove(elem)
            console.print("Der Auftrag wurde gelöscht!")
            save_orders_list(current_list)
            return
    console.print("Der Auftrag wurde nicht gefunden.")


@app.command()
def cleanup():
    removed_entries = 0

    current_list = get_orders_list()
    for elem in current_list:
        if elem.currentstatus and elem.currentstatus == "DELIVERED":
            current_list.remove(elem)
            removed_entries += 1
    save_orders_list(current_list)

    if removed_entries > 0:
        console.print(
            f"Es wurde {removed_entries}, die bereits geliefert wurden, gelöscht."
        )
    else:
        console.print("Es gab keinen Auftrag, der gelöscht werden konnte.")


if __name__ == "__main__":
    app()
