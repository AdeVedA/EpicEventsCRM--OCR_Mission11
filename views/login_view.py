import getpass

from validator.inputs import Input
from views.view import View


class LoginView:
    "View of the initial login part"

    @staticmethod
    def login_screen():
        header = "Client relations manager"
        menu_options = [
            "1. Login",
            "",
            "0. Exit",
        ]
        View.menu(header, menu_options)
        choice = input("\x1B[93m")
        return choice

    @staticmethod
    def get_login_data():
        """Recovers user connection information."""
        username = Input.string_name("Enter your username : ")
        password = getpass.getpass("\x1B[94mEnter your password : \x1B[0;0m")
        return username, password

    @staticmethod
    def firstscreen():
        """Welcome screen/program launch"""
        View.clear_screen()
        initial_screen = r"""
                           ___ ___ ___ ___
                          | __| _ \_ _/ __|
                          | _||  _/| | (__
                          |___|_| |___\___|
                     _____   _____ _  _ _____ ___
                    | __\ \ / / __| \| |_   _/ __|
                    | _| \ V /| _|| .` | | | \__ \
                    |___| \_/ |___|_|\_| |_| |___/"""
        View.prt_cyan(f"{initial_screen}")
        print("\n")
        View.input_return_prints("bienvenue")
