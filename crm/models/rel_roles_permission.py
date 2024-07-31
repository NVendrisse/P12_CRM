from peewee import ForeignKeyField
from crm.models.base import BaseModel
from crm.models.roles import Role
from crm.models.permission import Permission


class RelationRolesPermission(BaseModel):
    role = ForeignKeyField(model=Role)
    permission = ForeignKeyField(model=Permission)
