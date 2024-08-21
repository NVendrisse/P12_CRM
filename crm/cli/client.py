import typer
from peewee import DoesNotExist
from typing_extensions import Annotated
from crm.models.client import Client
from enum import Enum
from crm.utils.validator import check_mail
from crm.utils.display import table_display
from crm.utils.authentification import get_authenticated_user_id


client_app = typer.Typer()


class update_option(Enum):
    email = "email"
    phone = "phone"
    contact = "contact"


@client_app.command("create")
def create_client(
    name: Annotated[str, typer.Option(prompt=True)],
    surname: Annotated[str, typer.Option(prompt=True)],
    email: Annotated[str, typer.Option(prompt=True)],
    phone: Annotated[str, typer.Option(prompt=True)],
):
    """Create a client

    Args:
        name (Annotated[str, typer.Option, optional): Client name.)].
        surname (Annotated[str, typer.Option, optional): Client surname.)].
        email (Annotated[str, typer.Option, optional): Client email.)].
        phone (Annotated[str, typer.Option, optional): Client phone number.)].
    """
    if check_mail(email):
        client = Client(
            name=name,
            surname=surname,
            email=email,
            phone_number=phone,
            commercial_contact=get_authenticated_user_id(),
        )
        client.save()


@client_app.command("search")
def get_clients(
    name: Annotated[str, typer.Option()] = None,
    surname: Annotated[str, typer.Option()] = None,
    contact: Annotated[str, typer.Option()] = None,
):
    """Search for one or more clients based on three search option

    Args:
        name (Annotated[str, typer.Option, optional): client name. Defaults to None.
        surname (Annotated[str, typer.Option, optional): client surname. Defaults to None.
        contact (Annotated[str, typer.Option, optional): client contact. Defaults to None.
    """
    query = Client.select().where(
        (Client.name == name)
        | (Client.surname == surname)
        | (Client.commercial_contact == contact)
    )
    results = query.execute()
    table_display("Client query results", results)


@client_app.command("all")
def list_all_clients():
    """Return a list of all clients"""
    query = Client.select(Client.name, Client.surname, Client.commercial_contact)
    results = query.execute()
    table_display("All clients registered", results)


@client_app.command("update")
def update(
    name: Annotated[str, typer.Argument()],
    surname: Annotated[str, typer.Argument()],
    section: Annotated[update_option, typer.Argument()] = None,
    new_value: Annotated[str, typer.Argument()] = None,
):
    """Allow user to update one client

    Args:
        name (Annotated[str, typer.Argument): client name
        surname (Annotated[str, typer.Argument): client surname
        section (Annotated[update_option, typer.Argument, optional): section to update. Defaults to None.
        new_value (Annotated[str, typer.Argument, optional): new value for the selected section. Defaults to None.
    """
    client = Client.get((Client.name == name) & (Client.surname == surname))
    if (
        not section == None
        and not new_value == None
        and client.commercial_contact.id == get_authenticated_user_id()
    ):
        if section.value == "email":
            client.update_email(check_mail(new_value))
        elif section.value == "phone":
            client.update_phone_number(new_value)
        elif section.value == "contact":
            client.update_contact(new_value)
