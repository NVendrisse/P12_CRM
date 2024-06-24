from peewee import CharField
from .base import BaseModel


class Role(BaseModel):
    name = CharField()
