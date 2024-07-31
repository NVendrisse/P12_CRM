import peewee
from typer import Context
from crm.models.employee import Employee
from crm.models.rel_roles_permission import RelationRolesPermission as Relation
from crm.models.roles import Role
from crm.models.permission import Permission
from argon2 import PasswordHasher, exceptions
import jwt
from datetime import datetime, timedelta
import dotenv
from crm.utils.display import table_display


class BadCredential(Exception):
    msg = "Bad credential"


class UserIsNotConnected(Exception):
    msg = "You cannot perform this action because you are not connected"


def authenticate(login: str, password: str, output: bool = True):
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
            if output:
                dotenv.set_key(".env", "token", token)
            else:
                return True
        else:
            raise BadCredential
    except peewee.DoesNotExist:
        raise BadCredential
    except exceptions.VerifyMismatchError:
        raise BadCredential


def check(context: Context):
    if context.invoked_subcommand in ["login", "logout"]:
        return

    try:
        encrypted_token = dotenv.get_key(".env", "token")
        if not encrypted_token == None:
            token = jwt.decode(encrypted_token, "epicevent", algorithms=["HS256"])
            # debug
            print("///DEBUG///")
            print(f"command invoked : {context.invoked_subcommand}")
            print("///////////")
            # end debug
            set_user_permission(token["sub"])
        else:
            raise UserIsNotConnected

    except FileNotFoundError:
        print("File not found")


def set_user_permission(user_id: int):
    employee = Employee.get(Employee.id == user_id)
    employee.permissions = []
    query = Permission.select().join(Relation).where(Relation.role == employee.role)
    for perm in query:
        employee.permissions.append(perm.name)


def has_permission(function: str):
    return


def log_out():
    dotenv.unset_key(".env", "token")
