import typer
from peewee import DoesNotExist
from typing_extensions import Annotated, Optional
from crm.models.contract import Contract
from crm.utils.display import table_display, action_aborted, action_confirmed

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


@contract_app.command("sign")
def sign_contract(contract_id: Annotated[int, typer.Argument()] = None):
    contract = Contract.get(Contract.id == contract_id)
    signed = contract.sign()
    if signed:
        action_confirmed(f"Contract {contract.id} signed !")
    else:
        action_aborted(
            f"Cannot sign contract {contract.id}, maybe it is not fully payed"
        )


@contract_app.command("payment")
def update_balance(
    contract_id: Annotated[int, typer.Argument()] = None,
    set_balance: Annotated[float, typer.Option("-set")] = 0,
):
    contract = Contract.get(Contract.id == contract_id)
    contract.update_remaining_balance(set_balance)


@contract_app.command("search")
def get_contract(
    client: Annotated[int, typer.Option()] = None,
    contact: Annotated[int, typer.Option()] = None,
    payed: Annotated[bool, typer.Option()] = None,
    signed: Annotated[bool, typer.Option] = None,
):
    query = Contract.select().where(
        (Contract.is_cancelled == False)
        & (
            (Contract.client == client)
            | (Contract.contact == contact)
            | (Contract.is_payed == payed)
            | (Contract.is_signed == signed)
        )
    )
    results = query.execute()
    table_display("Contract query results", results)


@contract_app.command("delete")
def cancel_contract(contract_id: Annotated[int, typer.Argument()] = None):
    try:
        contract = Contract.get(Contract.id == contract_id)
        confirm = typer.confirm(
            f"Are you sure you want to delete the contract number : {contract.id} ?"
        )
        if confirm:
            contract.is_cancelled = True
            contract.save()
        else:
            action_aborted("Delete aborted")
    except DoesNotExist:
        return "There is no such contract with this number"
