from typer.testing import CliRunner
from crm.__main__ import epicevent_app
import pytest

runner = CliRunner()


def test_create_event():
    result = runner.invoke(
        epicevent_app,
        [
            "event",
            "create",
            "--contract",
            "1",
            "--client",
            "1",
            "--start",
            "10/10/2024",
            "--end",
            "12/10/2024",
            "--contact",
            "1",
            "--location",
            "Paris",
            "--attendees",
            "10",
            "--notes",
            "ok",
        ],
    )
    assert result.exit_code == 0


def test_get_event():
    result = runner.invoke(epicevent_app, ["event", "search", "--contact", "1"])
    assert result.exit_code == 0


def test_update_event():
    result = runner.invoke(
        epicevent_app, ["event", "update", "event_id", "1", "--notes", "ok ok ok"]
    )
    assert result.exit_code == 0
