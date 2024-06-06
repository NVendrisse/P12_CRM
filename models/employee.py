from peewee import CharField, DateField
from .base import BaseModel
from datetime import datetime
from argon2 import PasswordHasher


class Employee(BaseModel):
    login = CharField(unique=True)
    password = CharField()
    surname = CharField()
    name = CharField()
    date_created = DateField(default=datetime.now())

    def create(self):
        pass_hasher = PasswordHasher()
        self.password = pass_hasher.hash(password=self.password)
        return self.save()

    def update_password(self, new_password):
        self.password = new_password
        return self.create()
