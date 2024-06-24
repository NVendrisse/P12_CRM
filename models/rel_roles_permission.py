from peewee import ForeignKeyField
from .base import BaseModel
from models.roles import Role
from models.permission import Permission


class RelationRolesPermission(BaseModel):
    role = ForeignKeyField(model=Role)
    permission = ForeignKeyField(model=Permission)
