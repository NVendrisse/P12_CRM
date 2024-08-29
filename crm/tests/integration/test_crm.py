from crm.__main__ import epicevent_app
from typer.testing import CliRunner

runner = CliRunner()


def test_app(user):
    log = runner.invoke(
        epicevent_app, "crm user login --login fixture --password psswd"
    )
    assert log.exit_code == 0
