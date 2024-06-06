from peewee import SqliteDatabase, Model

app_database = SqliteDatabase("databases/epicevent.db")


class BaseModel(Model):
    class Meta:
        database = app_database
