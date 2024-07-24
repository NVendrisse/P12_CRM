from rich.console import Console
from rich.table import Table
from rich import print as rprint


def table_display(title: str = "", data=None):
    console = Console()
    table = Table(title=title)
    datatable = [*data]
    if len(datatable) > 0:
        for header in list(datatable[0].__dict__["__data__"].keys()):
            table.add_column(header.capitalize())
    for item in datatable:
        table.add_row(*[str(i) for i in list(item.__dict__["__data__"].values())])

    if table.columns:
        console.print(table)
    else:
        rprint("[bold red]No data found[/bold red]")


def action_confirmed(action: str):
    rprint(f"[bold bright_green]{action}[/bold bright_green]")


def action_aborted(action: str):
    rprint(f"[bold bright_red]{action}[/bold bright_red]")
