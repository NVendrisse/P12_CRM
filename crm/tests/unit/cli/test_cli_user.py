from typer.testing import CliRunner
from crm.__main__ import epicevent_app
from crm.models.employee import Employee
import pytest
import sqlite3


runner = CliRunner()
Employee.delete().where(Employee.login == "pytest").execute()


def test_login_valid_credential(user):
    result = runner.invoke(
        epicevent_app, ["user", "login", "--login", "fixture", "--password", "psswd"]
    )
    assert result.exit_code == 0


def test_login_invalid_credential(user):
    with pytest.raises(Exception) as e:
        result = runner.invoke(
            epicevent_app,
            ["user", "login", "--login", "fixture", "--password", "admin1"],
        )
        assert e.msg == "Bad credential"


def test_create_user(user):
    result = runner.invoke(
        epicevent_app,
        [
            "user",
            "create",
            "--login",
            "pytest",
            "--password",
            "12340",
            "--surname",
            "pytest",
            "--name",
            "testing",
            "--role",
            "3",
        ],
    )
    assert result.exit_code == 0


def test_list_user(user):
    result = runner.invoke(
        epicevent_app,
        [
            "user",
            "search",
            "--login",
            "fixture",
        ],
    )
    assert result.exit_code == 0


def test_change_user_password(user):
    result = runner.invoke(
        epicevent_app,
        [
            "user",
            "changepsw",
            "--login",
            "fixture",
            "--old_password",
            "psswd",
            "--new_password",
            "12345",
        ],
    )
    assert result.exit_code == 0


def test_rename_user(user):
    result = runner.invoke(
        epicevent_app,
        [
            "user",
            "rename",
            "--login",
            "fixture",
            "-n",
            "pytest",
        ],
    )
    assert result.exit_code == 0


def test_delete_user(user):
    result = runner.invoke(
        epicevent_app,
        [
            "user",
            "delete",
            "--login",
            "fixture",
        ],
    )
    assert result.exit_code == 0
