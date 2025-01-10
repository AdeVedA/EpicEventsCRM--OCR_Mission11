from sqlalchemy.exc import NoResultFound

from controllers.main_ctrl import MainController
from controllers.utils_ctrl import with_session
from models.models import User
from views.login_view import LoginView
from views.view import View


class LoginController:
    """Controller to manage the main login menu"""

    @staticmethod
    def run():
        LoginView.firstscreen()
        while True:
            choice = LoginView.login_screen()
            match choice:
                case "1":
                    try:
                        # Fetch user data
                        username, password = LoginView.get_login_data()
                        # Authenticate the user
                        try:
                            user = AuthController.login(username=username, password=password)
                            if user:
                                MainController(user).main()
                        except ValueError as e:
                            View.prt_red(f"Value error : {e}")
                            View.press_key()
                    except Exception as e:
                        View.prt_red(f"Unexpected error : {e}")
                        View.press_key()
                case "0":
                    View.input_return_prints("quit")
                    break
                case _:
                    View.input_return_prints("choice_error")


class AuthController:
    """controller for user authentication

    Raises:
        ValueError:

    Returns:
        The authenticated user object, or None if authentication fails.
    """

    @staticmethod
    @with_session
    def login(username, password, session=None):
        """Handles user login logic."""
        try:
            # Find the user in the database
            user = session.query(User).filter_by(username=username).one()
            # Check the password
            if user.check_password(password):
                return user
            else:
                raise ValueError("Incorrect password.")
        except (ValueError, NoResultFound):
            print("Wrong credentials")
