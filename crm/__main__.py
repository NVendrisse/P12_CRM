from typing_extensions import Annotated
import typer
from crm.utils.authentification import check
from crm.models.employee import Employee
from crm.cli.user import user_app


epicevent_app = typer.Typer()
epicevent_app.add_typer(user_app, name="user", callback=check)


if __name__ == "__main__":
    epicevent_app()
