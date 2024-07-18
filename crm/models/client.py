from peewee import CharField, DateField, ForeignKeyField
from .base import BaseModel
from .employee import Employee
from datetime import datetime


class Client(BaseModel):
    name = CharField()
    surname = CharField()
    email = CharField()
    phone_number = CharField()
    date_created = DateField(default=datetime.now())
    date_updated = DateField(default=datetime.now())
    commercial_contact = ForeignKeyField(model=Employee, backref="contact")

    def update_email(self, new_email: str):
        self.email = new_email
        self.date_updated = datetime.now()
        return self.save()

    def update_phone_number(self, new_number):
        self.phone_number = new_number
        self.date_updated = datetime.now()
        self.save()

    def update_contact(self, new_contact):
        self.commercial_contact = new_contact
        self.date_updated = datetime.now()
        self.save()
