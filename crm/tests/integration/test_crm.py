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
