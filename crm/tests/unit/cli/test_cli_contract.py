from typer.testing import CliRunner
from crm.__main__ import epicevent_app
import pytest

runner = CliRunner()


def test_create_contract(user):
    results = runner.invoke(
        epicevent_app,
        [
            "contract",
            "create",
            "--client",
            "1",
            "--contact",
            "1",
            "--cost",
            "100",
            "--remaining-balance",
            "0",
        ],
    )
    assert results.exit_code == 0


def test_sign_contract(user):
    results = runner.invoke(
        epicevent_app,
        [
            "contract",
            "sign",
            "1",
        ],
    )
    assert "signed" in results.stdout


def test_contract_payment(user):
    results = runner.invoke(
        epicevent_app,
        ["contract", "payment", "1", "-set", "0"],
    )
    assert results.exit_code == 0


def test_delete_contract(user):
    results = runner.invoke(epicevent_app, ["contract", "delete", "1"])
    assert results.exit_code == 0
