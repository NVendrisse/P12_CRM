from peewee import CharField
from crm.models.base import BaseModel


class Role(BaseModel):
    name = CharField()
