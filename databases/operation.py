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


def fill_database_default():

    perms = [
        "create_user",
        "search_user",
        "changepsw_user",
        "rename_user",
        "delete_user",
        "create_event",
        "search_event",
        "update_event",
        "create_contract",
        "sign_contract",
        "payment_contract",
        "search_contract",
        "delete_contract",
        "create_client",
        "search_client",
        "all_client",
        "update_client",
    ]

    Role(name="Management").save()
    Role(name="Support").save()
    Role(name="Commercial").save()
    Role(name="Admin").save()

    for permission in perms:
        Permission(name=permission, description="").save()

    management_perm = [1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    support_perm = [7, 8]
    commercial_perm = [6, 12, 14, 15, 16, 17]

    for perm_id in management_perm:
        RelationRolesPermission(role=1, permission=perm_id).save()

    for perm_id in support_perm:
        RelationRolesPermission(role=2, permission=perm_id).save()

    for perm_id in commercial_perm:
        RelationRolesPermission(role=3, permission=perm_id).save()

    for i in range(1, 19):
        RelationRolesPermission(role=4, permission=i).save()
