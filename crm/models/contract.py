from peewee import DateField, ForeignKeyField, FloatField, BooleanField
from crm.models.base import BaseModel
from datetime import datetime
from crm.models.employee import Employee
from crm.models.client import Client


class Contract(BaseModel):
    client = ForeignKeyField(model=Client)
    contact = ForeignKeyField(model=Employee)
    total_cost = FloatField()
    remaining_balance = FloatField()
    creation_date = DateField(default=datetime.now())
    update_date = DateField(default=datetime.now())
    is_signed = BooleanField(default=False)
    is_payed = BooleanField(default=False)
    is_cancelled = BooleanField(default=False)

    def update_remaining_balance(self, value: float):
        try:
            self.remaining_balance = value
            if self.remaining_balance <= 0:
                self.is_payed = True
            else:
                self.is_payed = False
            self.update_date = datetime.now()
        except ValueError:
            return
        return self.save()

    def sign(self):
        self.is_signed = True
        return self.is_signed

    def cancel(self):
        self.is_cancelled = True
