from crm.__main__ import epicevent_app
from typer.testing import CliRunner

runner = CliRunner()


def test_app(user):
    log = runner.invoke(
        epicevent_app,
        ["user", "login", "--login", "fixture", "--password", "psswd"],
    )
    assert "Logged successfully" in log.stdout
    log = runner.invoke(
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
    assert log.exit_code == 0
    log = runner.invoke(
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
    assert log.exit_code == 0
    log = runner.invoke(
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
            "0",
        ],
    )
    assert log.exception
