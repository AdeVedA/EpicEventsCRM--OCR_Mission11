from controllers.client_ctrl import ClientController
from controllers.contract_ctrl import ContractController
from controllers.event_ctrl import EventController
from controllers.user_ctrl import UserController
from views.main_view import MainMenuView
from views.view import View


class MainController:
    """Controller to manage the main role menu"""

    def __init__(self, user):
        self.user = user

    def main(self):
        """Main function to manage the role menu"""
        role = self.user.role.value
        if role == "MANAGEMENT":
            self.management_menu(self.user)
        elif role == "COMMERCIAL":
            self.commercial_menu(self.user)
        elif role == "SUPPORT":
            self.support_menu(self.user)
        else:
            View.input_return_prints("role_error")

    def management_menu(self, user):
        """Management menu function"""
        while True:
            choice = MainMenuView(user).managers_menu()
            match choice:
                case "1":
                    UserController(user).managers_collaborator_menu()
                case "2":
                    ContractController(user).managers_contract_menu()
                case "3":
                    EventController(user).managers_event_menu()
                case "4":
                    ClientController(user).list_clients()
                case "0":
                    break
                case _:
                    View.input_return_prints("choice_error")

    def commercial_menu(self, user):
        """Commercial menu function"""
        while True:
            choice = MainMenuView(user).commercials_menu()
            match choice:
                case "1":
                    ClientController(user).commercials_client_menu()
                case "2":
                    ContractController(user).commercials_contract_menu()
                case "3":
                    EventController(user).commercials_event_menu()
                case "0":
                    break
                case _:
                    View.input_return_prints("choice_error")

    def support_menu(self, user):
        """Support menu function"""
        while True:
            choice = MainMenuView(user).supports_menu()
            match choice:
                case "1":
                    EventController(user).supports_event_menu()
                case "2":
                    ContractController(user).list_contracts()
                case "3":
                    ClientController(user).list_clients()
                case "0":
                    break
                case _:
                    View.input_return_prints("choice_error")
