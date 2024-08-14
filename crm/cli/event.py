import typer
from peewee import DoesNotExist
from typing_extensions import Annotated, Optional
from crm.models.event import Event, ContractNotSigned
from crm.models.client import Client
from crm.utils.display import table_display
from crm.utils.authentification import get_authenticated_user_id

event_app = typer.Typer()


@event_app.command("create")
def create_event(
    contract: Annotated[int, typer.Option(prompt=True)],
    client: Annotated[int, typer.Option(prompt=True)],
    start: Annotated[str, typer.Option(prompt=True)],
    end: Annotated[str, typer.Option(prompt=True)],
    contact: Annotated[int, typer.Option(prompt=True)],
    location: Annotated[str, typer.Option(prompt=True)],
    attendees: Annotated[int, typer.Option(prompt=True)],
    notes: Annotated[str, typer.Option(prompt=True)],
):
    event = Event(
        contract=contract,
        client=client,
        start_date=start,
        end_date=end,
        commercial_contact=contact,
        location=location,
        attendees=attendees,
        notes=notes,
    )
    try:
        client_contact = Client.get(Client.id == client)
        if client_contact == get_authenticated_user_id():
            event.create_event()
        else:
            print(
                "It seems that you try to create an event but you are not the commercial contact associated with the client"
            )
    except ContractNotSigned as e:
        print(e.msg)


@event_app.command("search")
def get_event(
    contract: Annotated[int, typer.Option()] = None,
    client: Annotated[int, typer.Option()] = None,
    contact: Annotated[int, typer.Option()] = None,
):
    query = Event.select().where(
        (Event.contract == contract)
        | (Event.client == client)
        | (Event.commercial_contact == contact)
    )
    results = query.execute()
    table_display("Event query results", results)


@event_app.command("update")
def update_event(
    event_id: Annotated[int, typer.Argument()],
    contact: Annotated[int, typer.Option()] = None,
    notes: Annotated[str, typer.Option()] = None,
):
    event = Event.get(Event.id == event_id)
    if not contact == None:
        event.commercial_contact = contact
    if not notes == None:
        event.notes = notes
    event.save()
