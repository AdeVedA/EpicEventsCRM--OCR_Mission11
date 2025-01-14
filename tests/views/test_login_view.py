import pytest

from views.login_view import LoginView


def test_get_login_data(mocker):
    mocker.patch("validator.inputs.Input.string_name", side_effect=["testuser", "testpassword"])
    mocker.patch("getpass.getpass", return_value="testpassword")

    username, password = LoginView.get_login_data()
    assert username == "testuser"
    assert password == "testpassword"
