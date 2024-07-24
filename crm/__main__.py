import typer
from crm.utils.authentification import check
from crm.cli.user import user_app
from crm.cli.client import client_app
from crm.cli.contract import contract_app
from crm.cli.event import event_app


epicevent_app = typer.Typer()
epicevent_app.add_typer(user_app, name="user", callback=check)
epicevent_app.add_typer(client_app, name="client", callback=check)
epicevent_app.add_typer(contract_app, name="contract", callback=check)
epicevent_app.add_typer(event_app, name="event", callback=check)

if __name__ == "__main__":
    epicevent_app()
