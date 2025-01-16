import pytest

from views.user_view import UserView


@pytest.fixture
def user_view(mocker):
    """Fixture pour initialiser une UserView avec un utilisateur fictif."""
    mock_user = mocker.Mock(username="testmanager")
    return UserView(mock_user)


def test_managers_collaborator_show(user_view, mocker):
    """Teste la méthode managers_collaborator_show."""
    mocker.patch("builtins.input", return_value="1")
    result = user_view.managers_collaborator_show()
    assert result == "1", "La méthode n'a pas retourné le choix utilisateur."


def test_show_collaborators_empty(user_view, mocker):
    """Teste show_collaborators avec une liste vide."""
    mock_input_return_prints = mocker.patch("views.view.View.input_return_prints")
    user_view.show_collaborators([], update=False)
    mock_input_return_prints.assert_called_once_with("no_user")


def test_show_collaborators_with_data(user_view, mocker):
    """Teste show_collaborators avec des collaborateurs."""
    collaborators = [
        mocker.Mock(id=1, username="user1", role=mocker.Mock(value="COMMERCIAL")),
        mocker.Mock(id=2, username="user2", role=mocker.Mock(value="SUPPORT")),
    ]
    mock_menu = mocker.patch("views.view.View.menu")
    mock_table_show = mocker.patch("views.view.View.table_show")
    mock_input_return_prints = mocker.patch("views.view.View.input_return_prints")

    user_view.show_collaborators(collaborators, update=False)

    # Vérifier que le menu est affiché
    mock_menu.assert_called_once_with("Collaborators' List - Testmanager", [])
    # Vérifier que les données sont affichées sous forme de table
    mock_table_show.assert_called_once_with(
        "COLLABORATORS Table",
        ["ID", "Username", "Role"],
        [["1", "user1", "Commercial"], ["2", "user2", "Support"]],
        {"Username": {"justify": "left", "style": "bold magenta"}, "Role": {"style": "bold cyan"}},
    )
    # Vérifier que l'invite continue est appelée
    mock_input_return_prints.assert_called_once_with("continue")


def test_show_collaborators_with_update(user_view, mocker):
    """Teste show_collaborators avec update=True."""
    collaborators = [
        mocker.Mock(id=1, username="user1", role=mocker.Mock(value="COMMERCIAL")),
        mocker.Mock(id=2, username="user2", role=mocker.Mock(value="SUPPORT")),
    ]
    mock_table_show = mocker.patch("views.view.View.table_show")
    result = user_view.show_collaborators(collaborators, update=True)

    # Vérifier que les IDs sont retournés
    assert result == [1, 2]
    # Vérifier que les collaborateurs sont affichés
    mock_table_show.assert_called_once()


def test_get_collaborator_creation_data(user_view, mocker):
    """Teste get_collaborator_creation_data."""
    mock_input_string_name = mocker.patch("validator.inputs.Input.string_name", return_value="newuser")
    mock_input_role = mocker.patch("validator.inputs.Input.role", return_value="COMMERCIAL")
    mock_getpass = mocker.patch("getpass.getpass", side_effect=["password", "password"])

    result = user_view.get_collaborator_creation_data()

    assert result == {
        "username": "newuser",
        "password": "password",
        "role": "COMMERCIAL",
    }
    mock_input_string_name.assert_called_once_with("\x1B[94mUsername : \x1B[93m")
    mock_input_role.assert_called_once_with("role : \x1B[33m")
    assert mock_getpass.call_count == 2


def test_get_user_id(user_view, mocker):
    """Teste get_user_id."""
    mock_input_integer = mocker.patch("validator.inputs.Input.integer", return_value=1)
    result = user_view.get_user_id([1, 2, 3], action="update")
    assert result == 1
    mock_input_integer.assert_called_once_with("Enter the User ID update: ", [1, 2, 3])


def test_get_user_update_data(user_view, mocker):
    """Teste get_user_update_data."""
    mock_user = mocker.Mock(id=1, username="testuser", role=mocker.Mock(value="COMMERCIAL"))
    mock_input_string_name = mocker.patch("validator.inputs.Input.string_name", return_value="updateduser")
    mock_input_role = mocker.patch("validator.inputs.Input.role", return_value="SUPPORT")
    mock_getpass = mocker.patch("getpass.getpass", side_effect=["newpassword", "newpassword"])

    result = user_view.get_user_update_data(mock_user)

    assert result == {
        "username": "updateduser",
        "password": "newpassword",
        "role": "SUPPORT",
    }
    mock_input_string_name.assert_called_once_with("\x1B[94mNew Username : \x1B[93m", upd=True)
    mock_input_role.assert_called_once_with("\x1B[94mNew Role (MANAGEMENT, COMMERCIAL, SUPPORT) : \x1B[93m", upd=True)
    assert mock_getpass.call_count == 2


def test_confirm_user_delete(user_view, mocker):
    """Teste confirm_user_delete."""
    mock_collab = mocker.Mock(id=1, username="testuser", role=mocker.Mock(value="COMMERCIAL"))
    mock_input = mocker.patch("builtins.input", return_value="y")

    result = user_view.confirm_user_delete(mock_collab)

    assert result is True
    mock_input.assert_called_once()
