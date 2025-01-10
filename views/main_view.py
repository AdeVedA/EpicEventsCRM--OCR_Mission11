# from models.models import User
from views.view import View


class MainMenuView(View):
    """
    Controller to manage the views of the welcome and main menu
    """

    def __init__(self, user):
        self.user = user
        self.username = user.username

    # MANAGEMENT MENU
    def managers_menu(self):
        """Shows the managers menu"""
        username = self.username
        header = "Managers Menu -  " + str(username.capitalize())
        menu_options = [
            "1. Collaborators management",
            "",
            "2. Contracts management",
            "",
            "3. Events management",
            "",
            "4. Clients list",
            "",
            "",
            "0. Quit",
        ]
        View.menu(header, menu_options)
        choice = input()
        return choice

    # COMMERCIAL MENU
    def commercials_menu(self):
        """Shows the commercials menu"""
        header = "Commercials Menu - " + str(self.username.capitalize())
        menu_options = [
            "1. Clients management",
            "",
            "2. Contracts management",
            "",
            "3. Events management",
            "",
            "",
            "0. Quit",
        ]
        View.menu(header, menu_options)
        choice = input()
        return choice

    # SUPPORT MENU
    def supports_menu(self):
        """Shows the supports menu"""
        header = "Supports Menu - " + str(self.username.capitalize())
        menu_options = [
            "1. Events management",
            "",
            "2. Contracts list",
            "",
            "3. Clients list",
            "",
            "",
            "0. Quit",
        ]
        View.menu(header, menu_options)
        choice = input()
        return choice
