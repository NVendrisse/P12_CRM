from pytest import fixture
from peewee import SqliteDatabase
from crm.models.base import BaseModel
from crm.models.client import Client
from crm.models.contract import Contract
from crm.models.employee import Employee
from crm.models.event import Event
from crm.models.permission import Permission
from crm.models.rel_roles_permission import RelationRolesPermission
from crm.models.roles import Role
from databases.operation import fill_database_default


@fixture(scope="function")
def memory_database():
    try:
        db = SqliteDatabase(":memory:")
        MODELS = [
            Client,
            Contract,
            Employee,
            Event,
            Permission,
            RelationRolesPermission,
            Role,
        ]
        db.bind(MODELS)

        db.create_tables(MODELS)
        db.connect(True)
        fill_database_default()
        yield db
    finally:
        db.close()


@fixture(scope="session")
def models_database():
    try:
        db = SqliteDatabase(":memory:")
        MODELS = [
            Client,
            Contract,
            Employee,
            Event,
            Permission,
            RelationRolesPermission,
            Role,
        ]
        db.bind(MODELS)

        db.create_tables(MODELS)
        db.connect(True)
        yield db
    finally:
        db.close()


@fixture
def user(memory_database, contract, event, client):
    return_user = Employee()
    return_user.login = "fixture"
    return_user.password = "psswd"
    return_user.name = "test"
    return_user.surname = "fixt"
    return_user.role = 4
    return_user.create()
    yield return_user


@fixture
def contract(memory_database):
    return_contract = Contract(
        client=1, contact=1, total_cost=200, remaining_balance=0, is_payed=True
    )
    return_contract.save()
    yield return_contract


@fixture
def event(memory_database):
    return_event = Event(
        contract=1,
        client=1,
        start_date="10/10/2010",
        end_date="11/10/2010",
        commercial_contact=1,
        location="",
        attendees=40,
        notes="",
    )
    return_event.save()
    yield return_event


@fixture
def client(memory_database):
    return_client = Client(
        name="Lulu",
        surname="Stucru",
        email="lulu.stucru@yahoo.fr",
        phone_number="0605020304",
        commercial_contact=1,
    )
    return_client.save()
    yield return_client
