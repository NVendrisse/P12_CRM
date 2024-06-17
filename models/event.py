from peewee import CharField, DateField, IntegerField, ForeignKeyField
from .base import BaseModel
from datetime import datetime
from models.client import Client
from models.contract import Contract
from models.employee import Employee


class ContractNotSigned(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Event(BaseModel):
    contract = ForeignKeyField(model=Contract)
    client = ForeignKeyField(model=Client)
    start_date = DateField()
    end_date = DateField()
    commercial_contact = ForeignKeyField(model=Employee)
    location = CharField()
    attendees = IntegerField()
    notes = CharField()

    def create_event(self):
        if self.contract.is_signed:
            return self.save()
        else:
            raise ContractNotSigned
