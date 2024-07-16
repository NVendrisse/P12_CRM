import peewee
from typer import Context
from crm.models.employee import Employee
from argon2 import PasswordHasher
import jwt
from datetime import datetime, timedelta
import dotenv


class BadCredential(Exception):
    msg = "Bad credential"


class UserIsNotConnected(Exception):
    msg = "You cannot perform this action because you are not connected"


def authenticate(login: str, password: str):
    ph = PasswordHasher()
    try:
        query_user = Employee.get(Employee.login == login)
        hashed_pawword = query_user.password
        if ph.verify(hashed_pawword, password):

            payload_data = {
                "sub": query_user.id,
                "login": query_user.login,
                "exp": datetime.now() + timedelta(hours=3),
            }
            token = jwt.encode(payload=payload_data, key="epicevent", algorithm="HS256")
            dotenv.set_key(".env", "token", token)
        else:
            raise BadCredential
    except peewee.DoesNotExist:
        raise BadCredential


def check(context: Context):
    if context.invoked_subcommand in ["login", "logout"]:
        return

    try:
        encrypted_token = dotenv.get_key(".env", "token")
        if not encrypted_token == None:
            token = jwt.decode(encrypted_token, "epicevent", algorithms=["HS256"])
        else:
            raise UserIsNotConnected

    except FileNotFoundError:
        print("File not found")


def log_out():
    dotenv.unset_key(".env", "token")
