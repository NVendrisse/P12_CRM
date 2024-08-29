from typer.testing import CliRunner
from crm.__main__ import epicevent_app

runner = CliRunner()


def test_create_client(user):
    results = runner.invoke(
        epicevent_app,
        [
            "client",
            "create",
            "--name",
            "Lulu",
            "--surname",
            "Stucru",
            "--email",
            "lulu.stucru@gmail.com",
            "--phone",
            "0258963147",
        ],
    )
    assert results.exit_code == 0


def test_get_client(user):
    results = runner.invoke(
        epicevent_app,
        [
            "client",
            "search",
            "--name",
            "Lulu",
        ],
    )
    assert results.exit_code == 0


def test_get_all_client(user):
    results = runner.invoke(epicevent_app, ["client", "all"])
    assert results.exit_code == 0


def test_update_client(user):
    results = runner.invoke(
        epicevent_app,
        [
            "client",
            "update",
            "--name",
            "Lulu",
            "--surname",
            "Stucru",
            "--section",
            "phone",
            "--new_value",
            "0147258963",
        ],
    )
    assert results.exit_code == 0
