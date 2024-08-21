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


@fixture(scope="session")
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
        yield db
    finally:
        db.close()
