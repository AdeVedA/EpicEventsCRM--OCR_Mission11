import pytest

from controllers.user_ctrl import UserController
from models.models import User


@pytest.fixture
def user_controller(db_session, mocker):
    """Fixture pour initialiser un UserController."""
    print("Requêter testmanager user...")
    manager_user = db_session.query(User).filter_by(username="testmanager").first()
    if not manager_user:
        users = db_session.query(User).all()
        print(f"Users in the database: {[user.username for user in users]}")
        raise RuntimeError("Manager user not found. setup_users a un soucis ?")
    mocker.patch("controllers.user_ctrl.UserView")  # Mock UserView
    return UserController(manager_user)


def test_list_collaborators(db_session, setup_users, user_controller, mocker):
    """Test listing des collaborators."""
    # Vérifier les utilisateurs présents dans la base
    users = db_session.query(User).all()
    assert len(users) == 3, f"Expected 3 users, found {len(users)}: {[user.username for user in users]}"

    # Moquer la méthode show_collaborators
    mock_show_collaborators = mocker.patch.object(
        user_controller.view,
        "show_collaborators",  # Moquer uniquement la méthode appelée
        return_value=None,  # Elle ne retourne rien
    )

    # Appeler la méthode list_collaborators
    user_controller.list_collaborators(session=db_session)

    # Vérifier que show_collaborators a été appelée avec les bons paramètres
    mock_show_collaborators.assert_called_once_with(users, False)


def test_list_collaborators_with_update(db_session, setup_users, user_controller, mocker):
    """Test listing collaborators avec update=True."""
    users = db_session.query(User).all()

    mock_show_collaborators = mocker.patch.object(
        user_controller.view, "show_collaborators", return_value=[user.id for user in users]  # Simuler un retour d'IDs
    )

    # Appeler list_collaborators avec update=True
    result = user_controller.list_collaborators(session=db_session, update=True)

    # Vérifier que show_collaborators a été appelée avec update=True
    mock_show_collaborators.assert_called_once_with(users, True)

    # Vérifier que le résultat correspond aux IDs des utilisateurs
    assert result == [user.id for user in users]


def test_create_collaborator(db_session, user_controller, mocker):
    """Test créer un collaborator."""
    mocker.patch.object(
        user_controller.view,
        "get_collaborator_creation_data",
        return_value={"username": "newuser", "password": "newpassword", "role": "COMMERCIAL"},
    )
    user_controller.create_collaborator(session=db_session)
    new_user = db_session.query(User).filter_by(username="newuser").first()
    assert new_user is not None
    assert new_user.role.value == "COMMERCIAL"


def test_update_user(db_session, setup_users, user_controller, mocker):
    """Test updating a user's details."""
    user = db_session.query(User).filter_by(username="testcommercial").first()
    if not user:
        raise RuntimeError("User testcommercial not found. setup_users a un soucis ?")

    mocker.patch.object(user_controller.view, "get_user_id", return_value=user.id)
    mocker.patch.object(
        user_controller.view,
        "get_user_update_data",
        return_value={"username": "updateduser", "password": "updatedpassword"},
    )

    user_controller.update_user(session=db_session)

    updated_user = db_session.query(User).filter_by(id=user.id).first()
    assert updated_user.username == "updateduser"
    assert updated_user.check_password("updatedpassword")


def test_delete_user(db_session, setup_users, user_controller, mocker):
    """Test deleting a user."""
    user = db_session.query(User).filter_by(username="testsupport").first()
    if not user:
        raise RuntimeError("User testsupport not found. setup_users a un soucis ?")

    mocker.patch.object(user_controller.view, "get_user_id", return_value=user.id)
    mocker.patch.object(user_controller.view, "confirm_user_delete", return_value=True)

    user_controller.delete_user(session=db_session)

    deleted_user = db_session.query(User).filter_by(id=user.id).first()
    assert deleted_user is None


def test_get_users(db_session, setup_users, user_controller):
    """Test récupérer tous les users."""
    users = user_controller.get_users(session=db_session)
    assert len(users) == 3
    usernames = [user.username for user in users]
    assert "testmanager" in usernames
    assert "testcommercial" in usernames
    assert "testsupport" in usernames


def test_get_commercials(db_session, setup_users, user_controller):
    """Test récupérer seulement les commercials."""
    commercials = user_controller.get_commercials(session=db_session)
    assert len(commercials) == 1
    assert commercials[0].username == "testcommercial"


def test_get_supports(db_session, setup_users):
    """Test récupérer seulement les supports."""
    supports = UserController.get_supports(session=db_session)
    assert len(supports) == 1
    assert supports[0].username == "testsupport"
