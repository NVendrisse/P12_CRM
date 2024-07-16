from models.client import Client


def test_create_client():
    new_client = Client()
    new_client.name = "test_client"
    new_client.surname = "test_surname"
    new_client.email = "test@test.test"
    new_client.phone_number = "+330652418975"
    new_client.commercial_contact = 1
    assert new_client.save()


def test_get_client():
    client = Client.get(Client.name == "test_client")
    assert client.surname == "test_surname"


def test_update_client_email():
    client = Client.get(Client.name == "test_client")
    client.update_email("test@test.com")
    assert client.email == "test@test.com"


def test_update_client_phone():
    client = Client.get(Client.name == "test_client")
    client.update_phone_number("+333333333333")
    assert client.phone_number == "+333333333333"


def test_delete_client():
    delete_query = Client.delete().where(Client.name == "test_client")
    result = delete_query.execute()
    assert result
