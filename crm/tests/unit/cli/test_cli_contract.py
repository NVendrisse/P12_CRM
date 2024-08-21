from typer.testing import CliRunner
from crm.__main__ import epicevent_app
import pytest

runner = CliRunner()


def test_create_contract():
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
            "--remaining_balance",
            "10",
        ],
    )


def test_sign_contract():
    results = runner.invoke(
        epicevent_app,
        [
            "contract",
            "sign",
            "contract_id",
            "1",
        ],
    )
    assert results.exit_code == 0


def test_contract_payment():
    results = runner.invoke(
        epicevent_app,
        ["contract", "payment", "--contract_id", "1", "--set_balance", "0"],
    )
    assert results.exit_code == 0


def test_delete_contract():
    results = runner(epicevent_app, ["contract", "delete", "contract_id", "1"])
