from peewee import SqliteDatabase, Model
import os

try:
    app_database = SqliteDatabase("databases/epicevent.db")
except FileNotFoundError:
    db = os.open("databases/epicevent.db", "x")
    db.close()
finally:
    app_database = SqliteDatabase("databases/epicevent.db")


class BaseModel(Model):
    class Meta:
        database = app_database
