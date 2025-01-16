from validator.inputs import Input


def test_integer_input(mocker):
    mocker.patch("validator.inputs.Input._input", return_value="123")
    result = Input.integer("Enter a number: ")
    assert result == 123


def test_string_input(mocker):
    mocker.patch("validator.inputs.Input._input", return_value="test")
    result = Input.string("Enter a string: ")
    assert result == "test"


def test_email_input(mocker):
    mocker.patch("validator.inputs.Input._input", return_value="test@example.com")
    result = Input.email("Enter an email: ")
    assert result == "test@example.com"
