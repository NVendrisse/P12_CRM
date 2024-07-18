import typer
from peewee import DoesNotExist
from typing_extensions import Annotated, Optional
from crm.models.employee import Employee
from crm.models.roles import Role
from crm.utils.authentification import authenticate, log_out, BadCredential
from crm.utils.display import table_display

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
def list_user(
    login: Annotated[Optional[str], typer.Option()] = None,
    surname: Annotated[Optional[str], typer.Option()] = None,
    name: Annotated[Optional[str], typer.Option()] = None,
    role: Annotated[Optional[int], typer.Option()] = None,
):

    query = Employee.select().where(
        (Employee.login == login)
        | (Employee.surname == surname)
        | (Employee.name == name)
        | (Employee.role == role)
    )
    results = query.execute()
    table_display("Employee query results", results)


@user_app.command("update")
def update_user_password(
    login: Annotated[str, typer.Argument()],
    old_password: Annotated[str, typer.Option(prompt=True, hide_input=True)],
    new_password: Annotated[str, typer.Option(prompt=True, hide_input=True)],
):
    employee = Employee.get(Employee.login == login)
    if authenticate(login, old_password, False):
        employee.update_password(new_password)
    else:
        raise BadCredential


@user_app.command("delete")
def delete_employee(login: Annotated[str, typer.Argument()]):
    try:
        employee = Employee.get(Employee.login == login)
        confirm = typer.confirm(
            f"Are you sure you want to delete this user : '{employee.name} {employee.surname}' ?"
        )
        if confirm:
            query = Employee.delete().where(Employee.id == employee.id)
            query.execute()
        else:
            print("Delete aborted!")
    except DoesNotExist:
        return "There is no user with this login"
