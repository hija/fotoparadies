import typer

from fotoparadies import FotoparadiesStatus
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()


def _print_table_with_status(fp_stati: list[FotoparadiesStatus]):
    pass


@app.command
def status(shop: int, order: int):
    fp_status = FotoparadiesStatus(shop, order)


if __name__ == "__main__":
    app()
