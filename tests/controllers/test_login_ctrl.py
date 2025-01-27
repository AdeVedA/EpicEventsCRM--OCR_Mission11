import pytest

from controllers.login_ctrl import AuthController, LoginController
from views.view import View


@pytest.fixture
def mock_login_view(mocker):
    """Mock des méthodes de LoginView."""
    mocker.patch("views.login_view.LoginView.firstscreen")
    mocker.patch("views.login_view.LoginView.login_screen", side_effect=["1", "0"])
    mocker.patch("views.login_view.LoginView.get_login_data", return_value=("testmanager", "securepassword"))


@pytest.fixture
def mock_view(mocker, ret_prt_mock):
    """Mock des méthodes de View."""
    mocker.patch("views.view.View.prt_red")
    mocker.patch("views.view.View.press_key")


def test_run_quit(mocker, mock_login_view, mock_view):
    """Teste que run() quitte correctement après avoir affiché l'écran de connexion."""
    mocker.patch("controllers.login_ctrl.LoginController.login")
    LoginController.run()
    View.input_return_prints.assert_called_once_with("quit")


def test_run_authenticate_success(mocker, mock_login_view, db_session, setup_users):
    """Teste que run() gère correctement un login réussi."""
    mock_main_controller = mocker.patch("controllers.main_ctrl.MainController.main")
    mocker.patch(
        "controllers.login_ctrl.AuthController.authenticate",
        return_value=db_session.query(setup_users[0].__class__).filter_by(username="testmanager").first(),
    )

    LoginController.run()

    mock_main_controller.assert_called_once()


def test_authenticate_success(db_session, setup_users):
    """Teste la méthode de connexion pour une connexion réussie."""
    authenticated_user = AuthController.authenticate("testmanager", "securepassword", session=db_session)
    assert authenticated_user.username == "testmanager"
    assert authenticated_user.role.value == "MANAGEMENT"


def test_authenticate_incorrect_password(db_session, setup_users):
    """Teste la méthode de connexion avec un mot de passe incorrect."""
    with pytest.raises(ValueError, match="Wrong credentials"):
        AuthController.authenticate("testmanager", "wrongpassword", session=db_session)


def test_authenticate_user_not_found(db_session):
    """Teste la méthode de connexion lorsque l'utilisateur n'est pas trouvé."""
    with pytest.raises(ValueError, match="Wrong credentials"):
        AuthController.authenticate("unknownuser", "securepassword", session=db_session)


def test_authenticate_unexpected_exception(db_session, mocker):
    """Teste la méthode de connexion pour gérer les exceptions inattendues."""
    mocker.patch("controllers.login_ctrl.with_session", lambda f: f)

    mocker.patch.object(db_session, "query", side_effect=Exception("Database error"))

    with pytest.raises(Exception, match="Database error"):
        AuthController.authenticate("testmanager", "securepassword", session=db_session)
