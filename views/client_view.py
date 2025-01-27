from validator.inputs import Input
from views.view import View


class ClientView(View):
    def __init__(self, user):
        self.user = user
        self.username = user.username

    def commercials_client_show(self):
        "shows the commercial's client management menu"
        header = f"Clients Menu - {self.username.capitalize()}({self.user.id})"
        menu_options = [
            "1. Create a client",
            "",
            "2. Update clients",
            "",
            "3. List clients",
            "",
            "",
            "0. Back",
        ]
        View.menu(header, menu_options)
        choice = input()
        return choice

    def get_client_creation_data(self):
        """Ask the user for the data needed to create a client"""
        print("\x1b[1A\x1b[2K\x1B[35mPlease enter client informations")
        return {
            "full_name": Input.string_name("Full name : \x1B[33m"),
            "email": Input.email("Email : \x1B[33m"),
            "phone": Input.phone_number("Phone : \x1B[33m"),
            "company_name": Input.company_name("Company name : \x1B[33m"),
        }

    def show_clients(self, clients, list_returns=False):
        """displays a table of clients
        returns a list of clients_ids if list_returns=True"""
        if not clients:
            View.input_return_prints("no_client")
        else:
            View.menu("clients' List - " + str(self.username.capitalize()), [])
            columns = [
                "ID",
                "Full Name",
                "Email",
                "Phone",
                "Compagny Name",
                "Contact ID",
                "Creation Date",
                "Last Update",
            ]
            rows = []
            for client in clients:
                row = [
                    str(client.id),
                    str(client.full_name),
                    str(client.email),
                    str(client.phone),
                    str(client.company_name),
                    str(client.commercial_contact_id),
                    str(client.creation_date.strftime("%Y-%m-%d %H:%M:%S")),
                    str(client.last_update_date.strftime("%Y-%m-%d %H:%M:%S")),
                ]
                rows.append(row)
            options = {
                "Full Name": {"style": "bold magenta"},
                "Email": {"justify": "left", "style": "bold cyan"},
                "Phone": {"justify": "left", "style": "bold cyan"},
                "Compagny Name": {"justify": "left", "style": "orange1"},
                "Creation Date": {"justify": "left", "style": "green"},
                "Last Update": {"justify": "left", "style": "green"},
            }
            View.table_show("CLIENTS Table", columns, rows, options)
            if list_returns:
                return [client.id for client in clients]
            else:
                View.input_return_prints("continue")

    def get_client_id(self, clients_ids, action=None):
        """Ask the user for a Client ID among clients_ids possible ids."""
        return Input.integer(f"Enter the Client ID {action}: ", clients_ids)

    def get_client_update_data(self, client, commercials):
        """Ask the user for client fields to update."""
        View.menu("Client Update Datas - " + str(self.username.capitalize()), [])
        View.space(23)
        View.prt_info_blue(f"Updating Client ID:\x1B[0;0m \x1B[93m{client.id}")
        View.prt_yellow(f"Current Full Name: \x1B[35m{client.full_name}")
        View.prt_yellow(f"Current Email:     \x1B[36m{client.email}")
        View.prt_yellow(f"Current Phone:     \x1B[36m{client.phone}")
        View.prt_yellow(f"Current Compagny:  \x1B[36m{client.company_name}\n")
        View.prt_yellow(f"Current Commercial Contact ID: \x1B[36m{client.commercial_contact_id}")

        View.prt_info_blue(" --- Enter new values OR leave blank to keep current value --- \x1B[33;0m\n")
        updated_data = {}

        new_full_name = Input.string_name("\x1B[94mNew Full Name : \x1B[93m", upd=True)
        if new_full_name:
            updated_data["full_name"] = new_full_name

        new_email = Input.email("\x1B[94mNew email : \x1B[93m", upd=True)
        if new_email:
            updated_data["email"] = new_email

        new_phone = Input.phone_number("\x1B[94mNew phone number : \x1B[93m", upd=True)
        if new_phone:
            updated_data["phone"] = new_phone

        new_company_name = Input.company_name("\x1B[94mNew company_name : \x1B[93m", upd=True)
        if new_company_name:
            updated_data["company_name"] = new_company_name

        commercials_list = View.show_compact_list("Commercials", commercials, "username")
        new_commercial_contact_id = Input.integer(
            "\n\x1B[94mNew Commercial Contact ID : \x1B[93m", choices=commercials_list, upd=True
        )
        if new_commercial_contact_id:
            updated_data["commercial_contact_id"] = new_commercial_contact_id

        return updated_data
