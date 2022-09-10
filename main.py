import typer

from fotoparadies import FotoparadiesStatus
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()


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
def status(shop: int, order: int):
    fp_status = FotoparadiesStatus(shop, order)
    _print_table_with_status([fp_status])


if __name__ == "__main__":
    app()
