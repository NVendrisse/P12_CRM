from peewee import SqliteDatabase
from crm.models.client import Client
from crm.models.contract import Contract
from crm.models.employee import Employee
from crm.models.event import Event
from crm.models.permission import Permission
from crm.models.rel_roles_permission import RelationRolesPermission
from crm.models.roles import Role

MODELS = [
    Client,
    Contract,
    Employee,
    Event,
    Permission,
    RelationRolesPermission,
    Role,
]


def set_tables():
    app_database = SqliteDatabase("databases/epicevent.db")
    app_database.create_tables(MODELS)


def set_roles():
    Role(name="Management").save()
    Role(name="Support").save()
    Role(name="Commercial").save()
    Role(name="Admin").save()


def set_permissions():
    Permission(name="create_user", description="").save()
    Permission(name="create_user", description="").save()
    Permission(name="create_user", description="").save()
