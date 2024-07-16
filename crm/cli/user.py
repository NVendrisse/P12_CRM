import typer
from typing import Tuple
from typing_extensions import Annotated, Optional
from crm.models.employee import Employee
from crm.utils.authentification import authenticate, log_out

user_app = typer.Typer()


@user_app.command("login")
def login(
    login: Annotated[str, typer.Option(prompt=True)],
    password: Annotated[str, typer.Option(prompt=True, hide_input=True)],
):
    authenticate(login, password)


@user_app.command("logout")
def logout():
    try:
        log_out()
    except FileNotFoundError:
        pass


@user_app.command("create")
def create_user(
    login: Annotated[str, typer.Option(prompt=True)],
    password: Annotated[str, typer.Option(prompt=True)],
    surname: Annotated[str, typer.Option(prompt=True)],
    name: Annotated[str, typer.Option(prompt=True)],
    role: Annotated[int, typer.Option(prompt=True)],
):
    try:
        new_user = Employee()
        new_user.login = login
        new_user.password = password
        new_user.surname = surname
        new_user.name = name
        new_user.role = role
        new_user.create()
    except ValueError:
        print("error")  # ajouter texte


@user_app.command("search")
def get_user(
    login: Annotated[Optional[str], typer.Option()] = None,
    surname: Annotated[Optional[str], typer.Option()] = None,
    name: Annotated[Optional[str], typer.Option()] = None,
    role: Annotated[Optional[int], typer.Option()] = None,
):

    results = Employee.select().where(
        (Employee.login == login)
        ^ (Employee.surname == surname)
        ^ (Employee.name == name)
        ^ (Employee.role == role)
    )
    s = results.execute()
    print(len(s))
