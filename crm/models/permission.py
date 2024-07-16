from peewee import CharField
from crm.models.base import BaseModel


class Permission(BaseModel):
    name = CharField()
    description = CharField()
