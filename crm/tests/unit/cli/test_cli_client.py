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
            "Bana",
            "--surname",
            "Neplantain",
            "--email",
            "bana.neplantain@gmail.com",
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
            "Lulu",
            "Stucru",
            "phone",
            "0147258963",
        ],
    )
    assert results.exit_code == 0
