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
    pass


class UserIsNotConnected(Exception):
    msg = "You cannot perform this action because you are not connected"


class PermissionDenied(Exception):
    msg = "You do not have the permission to perform this action"


def authenticate(login: str, password: str, output: bool = True):
    """
    Validate the authentification query, with a password validation and create an auth token
    Then set a .env file and write the auth token to it

    The output arg, which is a boolean allow the programmer to use this function as a simple login validator,
    without the use of a jwt token
    """
    ph = PasswordHasher()
    try:
        query_user = Employee.get(Employee.login == login)
        hashed_password = query_user.password
        if ph.verify(hashed_password, password):

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
    """
    This function is checking the auth status of the current session,
    whenever a user is using a command it will check if a user is connected and if he has the right to execute this command
    """
    if context.invoked_subcommand in ["login", "logout", "create_default"]:
        return

    try:
        encrypted_token = dotenv.get_key(".env", "token")
        if not encrypted_token == None:
            token = jwt.decode(encrypted_token, "epicevent", algorithms=["HS256"])
            permission_needed = f"{context.invoked_subcommand}_{context.command.name}"
            if has_permission(token["sub"], permission_needed):
                return
            else:
                raise PermissionDenied
        else:
            raise UserIsNotConnected

    except FileNotFoundError:
        print("Authentification file not found, please contact an administrator")
    except jwt.ExpiredSignatureError:
        print("The session as expired please connect")


def has_permission(user_id: int, asked_permission: str):
    """
    Get the user, user roles and permission, and set them in the user instance
    """
    employee = Employee.get(Employee.id == user_id)
    employee.permissions = []
    query = Permission.select().join(Relation).where(Relation.role == employee.role)
    for perm in query:
        employee.permissions.append(perm.name)
    if asked_permission in employee.permissions:
        return True
    else:
        return False


def get_authenticated_user_id():
    """
    Get the actual autheticated user and return his id
    """
    try:
        encrypted_token = dotenv.get_key(".env", "token")
        if not encrypted_token == None:
            token = jwt.decode(encrypted_token, "epicevent", algorithms=["HS256"])
        return int(token["sub"])
    except FileNotFoundError:
        print("An internal error occured, please contact an administrator")


def log_out():
    dotenv.unset_key(".env", "token")
