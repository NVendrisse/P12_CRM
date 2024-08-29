from crm.models.contract import Contract


def test_create_contract(memory_database):
    new = Contract()
    new.client = 1
    new.contact = 1
    new.total_cost = 100.5
    new.remaining_balance = 19.5
    assert new.save()


def test_get_contract(memory_database):
    contract = Contract.get(Contract.id == 1)
    assert contract.total_cost == 1200


def test_get_multiple_contracts(memory_database):
    contracts = Contract.select().where(Contract.contact == 1)
    assert len(contracts) > 1


def test_update_balance(memory_database):
    contract = Contract.get(Contract.id == 1)
    contract.update_remaining_balance(100.90)
    assert contract.remaining_balance == 100.90


def test_sign_not_payed(memory_database):
    contract = Contract.get(Contract.id == 1)
    contract.sign()
    assert not contract.is_signed


def test_sign_payed(memory_database):
    contract = Contract.get(Contract.id == 1)
    contract.update_remaining_balance(0)
    contract.sign()
    assert contract.is_signed
