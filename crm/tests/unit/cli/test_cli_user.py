from typer.testing import CliRunner
from crm.__main__ import epicevent_app
from crm.models.employee import Employee
import pytest
import sqlite3


runner = CliRunner()
Employee.delete().where(Employee.login == "pytest").execute()


def test_login_valid_credential():
    result = runner.invoke(
        epicevent_app, ["user", "login", "--login", "admin", "--password", "admin"]
    )
    assert result.exit_code == 0


def test_login_invalid_credential():
    with pytest.raises(Exception) as e:
        result = runner.invoke(
            epicevent_app, ["user", "login", "--login", "admin", "--password", "admin1"]
        )
        assert e.msg == "Bad credential"


def test_create_user(memory_database):
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


def test_list_user():
    result = runner.invoke(
        epicevent_app,
        [
            "user",
            "search",
            "--login",
            "pytest",
        ],
    )
    assert result.exit_code == 0


def test_change_user_password():
    result = runner.invoke(
        epicevent_app,
        [
            "user",
            "changepsw",
            "--login",
            "pytest",
            "--old_password",
            "12340",
            "--new_password",
            "12345",
        ],
    )
    assert result.exit_code == 0


def test_rename_user():
    result = runner.invoke(
        epicevent_app,
        [
            "user",
            "rename",
            "--login",
            "pytest",
            "-n",
            "pytest",
        ],
    )
    assert result.exit_code == 0


def test_delete_user():
    result = runner.invoke(
        epicevent_app,
        [
            "user",
            "delete",
            "--login",
            "pytest",
        ],
    )
    assert result.exit_code == 0
