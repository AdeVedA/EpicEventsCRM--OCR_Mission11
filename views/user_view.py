import getpass

from validator.inputs import Input
from views.view import View


class UserView(View):
    def __init__(self, user):
        self.user = user
        self.username = user.username

    # USER MANAGEMENT MENU
    def managers_collaborator_show(self):
        """Shows the managers menu"""
        username = self.username
        header = "Collaborators Menu -  " + str(username.capitalize())
        menu_options = [
            "1. List collaborators",
            "2. Create collaborator",
            "3. Update collaborator",
            "4. Delete collaborator",
            "",
            "0. Back",
        ]
        View.menu(header, menu_options)
        choice = input()
        return choice

    def show_collaborators(self, collaborators, update):
        "print a table of collaborators"
        if not collaborators:
            View.input_return_prints("no_user")
        else:
            View.menu("Collaborators' List - " + str(self.username.capitalize()), [])
            columns = [
                "ID",
                "Username",
                "Role",
            ]
            rows = []
            sorted_collaborators = sorted(collaborators, key=lambda x: x.role.value)
            for collaborator in sorted_collaborators:
                row = [
                    str(collaborator.id),
                    str(collaborator.username),
                    str(collaborator.role.value.capitalize()),
                ]
                rows.append(row)
            options = {
                "Username": {"justify": "left", "style": "bold magenta"},
                "Role": {"style": "bold cyan"},
            }
            View.table_show("COLLABORATORS Table", columns, rows, options)
            if update:
                return [collaborator.id for collaborator in collaborators]
            else:
                View.input_return_prints("continue")

    def get_collaborator_creation_data(self):
        """Ask the user for the data needed to create a collaborator."""
        View.menu("Collaborator Creation - " + str(self.username.capitalize()), [])
        View.space(15)
        View.prt_info_blue("Please enter collaborator informations")
        username = Input.string_name("\x1B[94mUsername : \x1B[93m")
        is_valid = False
        while not is_valid:
            password = getpass.getpass("\x1B[94mEnter password : ")
            confirm_password = getpass.getpass("\x1B[94mConfirm password : ")
            if password != confirm_password:
                View.input_return_prints("passwords_not_match")
                View.erase_line(2)
            else:
                is_valid = True
        role = Input.role("role : \x1B[33m")
        return {
            "username": username,
            "password": password,
            "role": role,
        }

    def get_user_id(self, collabs_ids, action=None):
        """Ask the user for a User ID among collabs_ids possible ids."""
        return Input.integer(f"Enter the User ID {action}: ", collabs_ids)

    def get_user_update_data(self, user):
        """Ask the user for fields to update."""
        View.menu("User Update Datas - " + str(self.username.capitalize()), [])
        # print("\x1b[A\x1b[2K\x1b[A")
        View.space(23)
        View.prt_info_blue(f"Updating User ID:\x1B[0;0m \x1B[93m{user.id}")
        View.prt_yellow(f"Current Username: \x1B[95m{user.username}")
        View.prt_yellow(f"Current Role:     \x1B[96m{user.role.value}\n")

        View.prt_info_blue(" --- Enter new values OR leave blank to keep current value --- \x1B[33;0m\n")
        updated_data = {}

        new_username = Input.string_name("\x1B[94mNew Username : \x1B[93m", upd=True)
        if new_username:
            updated_data["username"] = new_username

        is_valid = False
        while not is_valid:
            new_password = getpass.getpass("\x1B[94mNew password : ")
            if new_password == "":
                break
            confirm_password = getpass.getpass("\x1B[94mConfirm new password : ")
            if new_password != confirm_password:
                View.input_return_prints("passwords_not_match")
                View.erase_line(2)
            else:
                if new_password:
                    updated_data["password"] = new_password
                is_valid = True

        new_role = Input.role("\x1B[94mNew Role (MANAGEMENT, COMMERCIAL, SUPPORT) : \x1B[93m", upd=True)
        if new_role:
            updated_data["role"] = new_role

        return updated_data

    def confirm_user_delete(self, collab):
        """confirm the intention to delete given collaborator"""
        answer = (
            input(
                (
                    f"Are you sure you want to delete collaborator\n\x1B[95m{collab.username}\x1B[33m "
                    f"(id \x1B[94m{collab.id}\x1B[33m) from the \x1B[96m{collab.role.value}\x1B[33m team ?"
                    f"\n\x1B[91m(y/n) : "
                )
            )
            .strip()
            .lower()
        )
        return answer == "y"
