from peewee import CharField, DateField, ForeignKeyField
from crm.models.base import BaseModel
from datetime import datetime
from argon2 import PasswordHasher
from crm.models.roles import Role


class Employee(BaseModel):
    login = CharField(unique=True)
    password = CharField()
    surname = CharField()
    name = CharField()
    date_created = DateField(default=datetime.now())
    role = ForeignKeyField(model=Role, null=True)

    permissions = []

    def create(self):
        pass_hasher = PasswordHasher()
        self.password = pass_hasher.hash(password=self.password)
        return self.save()

    def update_password(self, new_password):
        self.password = new_password
        return self.create()
