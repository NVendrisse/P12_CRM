from peewee import CharField, DateField, IntegerField, ForeignKeyField
from crm.models.base import BaseModel
from datetime import datetime
from crm.models.client import Client
from crm.models.contract import Contract
from crm.models.employee import Employee


class ContractNotSigned(Exception):
    msg = "The contract attributed to this event is not signed, cannot create this event, please check the contract before creating this event again"


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
