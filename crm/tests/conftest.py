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


@fixture
def user(memory_database):
    return_user = Employee()
    return_user.login = "fixture"
    return_user.password = "psswd"
    return_user.name = "test"
    return_user.surname = "fixt"
    return_user.role = 4
    return_user.create()
    yield return_user
