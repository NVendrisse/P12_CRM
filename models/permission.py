from peewee import CharField
from .base import BaseModel


class Permission(BaseModel):
    name = CharField()
    description = CharField()
