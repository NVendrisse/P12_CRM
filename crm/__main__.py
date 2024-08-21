import typer
from peewee import OperationalError
from crm.utils.authentification import (
    check,
    BadCredential,
    UserIsNotConnected,
    PermissionDenied,
)
from crm.cli.user import user_app
from crm.cli.client import client_app
from crm.cli.contract import contract_app
from crm.cli.event import event_app
from databases.operation import set_tables


epicevent_app = typer.Typer()
epicevent_app.add_typer(
    user_app, name="user", help="User related commands", callback=check
)
epicevent_app.add_typer(
    client_app, name="client", help="Client related commands", callback=check
)
epicevent_app.add_typer(
    contract_app, name="contract", help="Contract related command", callback=check
)
epicevent_app.add_typer(
    event_app, name="event", help="Event related commands", callback=check
)

if __name__ == "__main__":
    try:
        epicevent_app()
    except BadCredential as b:
        print(b.msg)
    except UserIsNotConnected as u:
        print(u.msg)
    except PermissionDenied as p:
        print(p.msg)
    except OperationalError:
        set_tables()
