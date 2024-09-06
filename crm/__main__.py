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
from databases.operation import set_tables, fill_database_default
import sentry_sdk

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

sentry_sdk.init(
    dsn="https://e0d4fb09adf702b25cdb2da39cf36476@o4507448396218368.ingest.de.sentry.io/4507855997960272",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    debug=False,
)

if __name__ == "__main__":
    try:
        epicevent_app()
    except BadCredential as b:
        sentry_sdk.capture_exception(b)

    except UserIsNotConnected as u:
        sentry_sdk.capture_exception(u)
        print(u.msg)
    except PermissionDenied as p:
        sentry_sdk.capture_exception(p)
        print(p.msg)
    except OperationalError as o:
        sentry_sdk.capture_exception(o)
        print(
            "An error occured with the database, creating a new one to maintain the application, please contact as soon as possible an administrator"
        )
        set_tables()
        fill_database_default()
    except Exception as excep:
        sentry_sdk.capture_exception(excep)
