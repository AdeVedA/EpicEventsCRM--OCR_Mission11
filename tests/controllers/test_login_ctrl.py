import pytest

from controllers.login_ctrl import AuthController


def test_login_success(db_session, setup_users):
    """Test the login method for a successful login."""
    authenticated_user = AuthController.login("testmanager", "securepassword", session=db_session)
    assert authenticated_user.username == "testmanager"
    assert authenticated_user.role.value == "MANAGEMENT"


def test_login_incorrect_password(db_session, setup_users):
    """Test the login method with an incorrect password."""
    with pytest.raises(ValueError, match="Wrong credentials"):
        AuthController.login("testmanager", "wrongpassword", session=db_session)


def test_login_user_not_found(db_session):
    """Test the login method when the user is not found."""
    with pytest.raises(ValueError, match="Wrong credentials"):
        AuthController.login("unknownuser", "securepassword", session=db_session)


def test_login_unexpected_exception(db_session, mocker):
    """Test the login method for handling unexpected exceptions."""
    mocker.patch("controllers.login_ctrl.with_session", lambda f: f)

    mocker.patch.object(db_session, "query", side_effect=Exception("Database error"))

    with pytest.raises(Exception, match="Database error"):
        AuthController.login("testmanager", "securepassword", session=db_session)
