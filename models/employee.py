from peewee import SqliteDatabase, CharField, DateField, Model

ee_database = SqliteDatabase("databases/epicevent.db")


class Employee(Model):
    login = CharField()
    password = CharField()
    surname = CharField()
    name = CharField()
    date_created = DateField()

    class Meta:
        database = ee_database
