from views.view import View


def test_press_key(mocker):
    mocker.patch("builtins.input", return_value="")
    View.press_key()


def test_input_return_prints_continue(mocker):
    mocker.patch("builtins.input", return_value="")
    View.input_return_prints("continue")


def test_input_return_prints_choice_error(mocker):
    mocker.patch("builtins.input", return_value="")
    View.input_return_prints("choice_error")


def test_input_return_prints_forbidden(mocker):
    mocker.patch("builtins.input", return_value="")
    View.input_return_prints("forbidden")


def test_input_return_prints_passwords_not_match(mocker):
    mocker.patch("builtins.input", return_value="")
    View.input_return_prints("passwords_not_match")


def test_input_return_prints_user_delete_cancel(mocker):
    mocker.patch("builtins.input", return_value="")
    View.input_return_prints("user_delete", "cancel")


def test_input_return_prints_user_delete_except(mocker):
    mocker.patch("builtins.input", return_value="")
    View.input_return_prints("user_delete", "except", "Error")


def test_input_return_prints_user_delete_ok(mocker):
    mocker.patch("builtins.input", return_value="")
    View.input_return_prints("user_delete", "ok", "testuser")


def test_input_return_prints_no_user(mocker):
    mocker.patch("builtins.input", return_value="")
    View.input_return_prints("no_user")


def test_input_return_prints_client_saved(mocker):
    mocker.patch("builtins.input", return_value="")
    View.input_return_prints("client_saved", "Test Client")


def test_input_return_prints_no_client(mocker):
    mocker.patch("builtins.input", return_value="")
    View.input_return_prints("no_client")


def test_input_return_prints_no_contract(mocker):
    mocker.patch("builtins.input", return_value="")
    View.input_return_prints("no_contract")


def test_input_return_prints_contract_saved(mocker):
    mocker.patch("builtins.input", return_value="")
    View.input_return_prints("contract_saved", 1, "Test Client")


def test_input_return_prints_no_event(mocker):
    mocker.patch("builtins.input", return_value="")
    View.input_return_prints("no_event")


def test_input_return_prints_event_saved(mocker):
    mocker.patch("builtins.input", return_value="")
    View.input_return_prints("event_saved", 1, "Test Event")


def test_input_return_prints_event_support_saved_cancel(mocker):
    mocker.patch("builtins.input", return_value="")
    View.input_return_prints("event_support_saved", "cancel")


def test_input_return_prints_event_support_saved_ok(mocker):
    mocker.patch("builtins.input", return_value="")
    View.input_return_prints("event_support_saved", "ok", "Test Event", "supportuser")


def test_input_return_prints_bienvenue(mocker):
    mocker.patch("builtins.input", return_value="")
    View.input_return_prints("bienvenue")


def test_input_return_prints_quit(mocker):
    mocker.patch("builtins.input", return_value="")
    View.input_return_prints("quit")
