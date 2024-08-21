from crm.models.employee import Employee


def test_create_employee():
    new_employee = Employee()
    new_employee.login = "test"
    new_employee.password = "password1234"
    new_employee.surname = "surname"
    new_employee.name = "name"
    assert new_employee.create()


def test_read_employee():
    get_employee = Employee.get(Employee.login == "test")
    assert get_employee.name == "name"


def test_update_password():
    get_employee = Employee.get(Employee.login == "test")
    assert get_employee.update_password("azerty12342")


def test_delete_employee():
    delete_employee = Employee.delete().where(Employee.login == "test")
    query = delete_employee.execute()
    assert query == 1
