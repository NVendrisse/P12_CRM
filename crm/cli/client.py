import typer
from peewee import DoesNotExist
from typing_extensions import Annotated, Optional
from crm.models.client import Client
from enum import Enum
from crm.utils.validator import check_mail
from crm.utils.display import table_display


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
    contact: Annotated[str, typer.Option(prompt=True)],
):
    if check_mail(email):
        client = Client(
            name=name,
            surname=surname,
            email=email,
            phone_number=phone,
            commercial_contact=contact,
        )
        client.save()


@client_app.command("search")
def get_clients(
    name: Annotated[str, typer.Option()] = None,
    surname: Annotated[str, typer.Option()] = None,
    contact: Annotated[str, typer.Option()] = None,
):

    query = Client.select().where(
        (Client.name == name)
        | (Client.surname == surname)
        | (Client.commercial_contact == contact)
    )
    results = query.execute()
    table_display("Client query results", results)


@client_app.command("all")
def list_all_clients():
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
    client = Client.get((Client.name == name) & (Client.surname == surname))
    if not section == None and not new_value == None:
        if section.value == "email":
            client.update_email(check_mail(new_value))
        elif section.value == "phone":
            client.update_phone_number(new_value)
        elif section.value == "contact":
            client.update_contact(new_value)


@client_app.command("delete")
def delete(
    name: Annotated[str, typer.Argument()], surname: Annotated[str, typer.Argument()]
):
    try:
        client = Client.get((Client.name == name) & (Client.surname == surname))
        confirm = typer.confirm(
            f"Are you sure you want to delete this client : '{client.name} {client.surname}' ?"
        )
        if confirm:
            query = Client.delete().where(Client.id == client.id)
            query.execute()
        else:
            print("Delete aborted")
    except DoesNotExist as e:
        print(e)
