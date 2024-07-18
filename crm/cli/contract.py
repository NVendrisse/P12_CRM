import typer
from peewee import DoesNotExist
from typing_extensions import Annotated, Optional
from crm.models.contract import Contract
from crm.utils.display import table_display

contract_app = typer.Typer()


@contract_app.command("create")
def create_contract(
    client: Annotated[int, typer.Option(prompt=True)],
    contact: Annotated[int, typer.Option(prompt=True)],
    cost: Annotated[int, typer.Option(prompt=True)],
    remaining_balance: Annotated[int, typer.Option(prompt=True)],
):
    contract = Contract(
        client=client,
        contact=contact,
        total_cost=cost,
        remaining_balance=remaining_balance,
    )
    if remaining_balance == 0:
        contract.is_payed = True
    contract.save()
    print("Contract created, remember to sign it before using it")
