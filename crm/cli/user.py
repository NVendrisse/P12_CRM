import typer
from peewee import DoesNotExist
from typing_extensions import Annotated, Optional
from crm.models.employee import Employee
from crm.models.employee import Role
from crm.models.roles import Role
from crm.utils.authentification import (
    authenticate,
    log_out,
    get_authenticated_user_id,
    BadCredential,
)
from crm.utils.display import table_display, action_aborted, action_confirmed

user_app = typer.Typer()


@user_app.command("create_default")
def default_user():
    user = Employee()
    user.login = "default"
    user.password = "password"
    user.surname = ""
    user.name = ""
    user.role = 1
    user.create()


@user_app.command("login")
def login(
    login: Annotated[str, typer.Option(prompt=True)],
    password: Annotated[str, typer.Option(prompt=True, hide_input=True)],
):
    """Log the user

    Args:
        login (Annotated[str, typer.Option, optional): login of the user. Defaults to True)].
        password (Annotated[str, typer.Option, optional): password of the user. Defaults to True, hide_input=True)].
    """
    try:
        authenticate(login, password)
        action_confirmed("Logged successfully")
    except BadCredential:
        action_aborted("You have enterred a wrong login or password")
        raise BadCredential


@user_app.command("logout")
def logout():
    """Log out the current user"""
    try:
        log_out()
        action_confirmed("Logged out!")
    except FileNotFoundError:
        action_aborted("Oops an error occured try to log in again")


@user_app.command("create")
def create_user(
    login: Annotated[str, typer.Option(prompt=True)],
    password: Annotated[str, typer.Option(prompt=True)],
    surname: Annotated[str, typer.Option(prompt=True)],
    name: Annotated[str, typer.Option(prompt=True)],
    role: Annotated[int, typer.Option(prompt=True)],
):
    """Create a new user

    Args:
        login (Annotated[str, typer.Option, optional): login of the new user. Defaults to True)].
        password (Annotated[str, typer.Option, optional): new default password for the user. Defaults to True)].
        surname (Annotated[str, typer.Option, optional): new user surname. Defaults to True)].
        name (Annotated[str, typer.Option, optional): new user name. Defaults to True)].
        role (Annotated[int, typer.Option, optional): new user role. Defaults to True)].
    """
    try:
        new_user = Employee()
        new_user.login = login
        new_user.password = password
        new_user.surname = surname
        new_user.name = name
        new_user.role = role
        new_user.create()
        action_confirmed(f"{new_user.surname} {new_user.name} created succesfully!")
    except ValueError:
        action_aborted(
            "One or more value you have entered is not correct, please try again"
        )


@user_app.command("search")
def list_user(
    login: Annotated[Optional[str], typer.Option()] = None,
    surname: Annotated[Optional[str], typer.Option()] = None,
    name: Annotated[Optional[str], typer.Option()] = None,
    role: Annotated[Optional[int], typer.Option()] = None,
):

    query = Employee.select(
        Employee.login, Employee.name, Employee.surname, Employee.role
    ).where(
        (Employee.login == login)
        | (Employee.surname == surname)
        | (Employee.name == name)
        | (Employee.role == role)
    )
    results = query.execute()
    table_display("Employee query results", results)


@user_app.command("changepsw")
def update_user_password(
    login: Annotated[str, typer.Argument()],
    old_password: Annotated[str, typer.Option(prompt=True, hide_input=True)] = None,
    new_password: Annotated[str, typer.Option(prompt=True, hide_input=True)] = None,
):
    """Allow the connected user to change his password

    Args:
        login (Annotated[str, typer.Argument): Login of the user which the password will be changed
        old_password (Annotated[str, typer.Option, optional): old user password. Defaults to True, hide_input=True)]=None.
        new_password (Annotated[str, typer.Option, optional): new user password. Defaults to True, hide_input=True)]=None.

    Raises:
        BadCredential: _description_
    """
    employee = Employee.get(Employee.login == login)
    if (
        authenticate(login, old_password, False)
        and employee.id == get_authenticated_user_id()
    ):
        if not new_password == None:
            employee.update_password(new_password)
            action_confirmed("Password changed")
    else:
        action_aborted(
            "You have entered the wrong original password, or maybe you are not the user you try to update"
        )


@user_app.command("rename")
def rename_user(
    login: Annotated[str, typer.Argument()],
    new_name: Annotated[str, typer.Option("-n")] = None,
    new_surname: Annotated[str, typer.Option("-s")] = None,
):
    """Aloow user to be renamed

    Args:
        login (Annotated[str, typer.Argument): user login
        new_name (Annotated[str, typer.Option, optional): new name for this user. Defaults to None.
        new_surname (Annotated[str, typer.Option, optional): new surname for this user. Defaults to None.
    """
    employee = Employee.get(Employee.login == login)
    if new_name is not None:
        employee.name = new_name
    if new_surname is not None:
        employee.surname = new_surname
    employee.save()


@user_app.command("delete")
def delete_employee(login: Annotated[str, typer.Argument()]):
    """Unactivate a user account

    Args:
        login (Annotated[str, typer.Argument): login of the user to disactivate

    """
    try:
        employee = Employee.get(Employee.login == login)
        confirm = typer.confirm(
            f"Are you sure you want to delete this user : '{employee.name} {employee.surname}' ?"
        )
        if confirm:
            employee.is_active = False
            employee.save()
        else:
            action_aborted("Delete aborted")
    except DoesNotExist:
        return "There is no user with this login"
