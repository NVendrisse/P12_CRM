from crm.__main__ import epicevent_app
from typer.testing import CliRunner

runner = CliRunner()


def test_app():
    log = runner.invoke(epicevent_app, "crm user login --login admin --password admin")
    assert log.exit_code == 0
