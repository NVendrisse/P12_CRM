from crm.models.event import Event


def test_create_event(models_database):
    event = Event()
    event.contract = 1
    event.client = 1
    event.start_date = "10/12/2024"
    event.end_date = "11/12/2024"
    event.commercial_contact = 1
    event.location = "Amsterdam"
    event.attendees = 100
    event.notes = "None"
    assert event.create_event()


def test_get_event(models_database):
    event = Event.get(Event.location == "Amsterdam")
    assert event.attendees == 100


def test_update_event(models_database):
    event = Event.get(Event.notes == "None")
    event.attendees = 150
    assert event.save()


def test_delete_event(models_database):
    query = Event.delete().where(Event.location == "Amsterdam")
    assert query.execute()
