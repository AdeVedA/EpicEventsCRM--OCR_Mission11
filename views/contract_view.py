from validator.inputs import Input
from views.error_view import ErrorView
from views.view import View


class ContractView(View):
    def __init__(self, user):
        self.user = user
        self.username = user.username

    def managers_contract_show(self):
        "shows the manager's contract management menu"
        header = f"Contract Menu - {self.username.capitalize()}"
        menu_options = [
            "1. List contracts",
            "2. Create contracts",
            "3. Update contract",
            "",
            "0. Back",
        ]
        View.menu(header, menu_options)
        choice = input()
        return choice

    def commercials_contract_show(self):
        "shows the commercial's contract management menu"
        header = f"Contract Menu - {self.username.capitalize()}"
        menu_options = [
            "1. List contracts",
            "2. Update my client's contract",
            "3. Display unsigned contracts",
            "4. Display unpaid contracts",
            "",
            "0. Back",
        ]
        View.menu(header, menu_options)
        choice = input()
        return choice

    def get_contract_creation_data(self, clients, commercials):
        """Ask the user for the data needed to create a contract"""
        View.menu("Contract Creation - " + str(self.username.capitalize()), [])
        View.space(17)
        View.prt_info_blue("Please enter contract informations")
        # Show compact lists for clients and commercials
        clients_list = View.show_compact_list("Here are the registered clients : ", clients, "full_name")
        client_id = Input.integer("\nSelect a Client ID from the list: \x1B[33m", clients_list)

        commercials_list = View.show_compact_list("Here are the commercials", commercials, "username")
        commercial_contact_id = Input.integer(
            "\nSelect a Commercial Contact ID from the list: \x1B[33m", commercials_list
        )

        # total_amount has to be a positive number
        is_valid = False
        while not is_valid:
            total_amount = Input.float("Total Amount: \x1B[33m")
            if total_amount < 0.0:
                ErrorView.alert("the bill total amount can't be negative")
                continue
            is_valid = True
        # remaining_amount has to be lower than total_amount
        remaining_amount = Input.float("Remaining Amount: \x1B[33m", limit=total_amount)

        status = Input.signed_contract("Status (signed or unsigned): \x1B[33m")
        return {
            "client_id": client_id,
            "commercial_contact_id": commercial_contact_id,
            "total_amount": total_amount,
            "remaining_amount": remaining_amount,
            "status": status,
        }

    def show_contracts(self, contracts, list_returns=False):
        """displays contracts table (and return list of contracts if list_returns=True)"""
        if not contracts:
            View.input_return_prints("no_contract")
        else:
            View.menu("Contracts' List - " + str(self.username.capitalize()), [])
            columns = [
                "ID",
                "Client ID",
                "Status",
                "Remaining Amount",
                "Total Amount",
                "Creation Date",
                "Commercial Contact ID",
            ]
            rows = []
            for contract in contracts:
                row = [
                    str(contract.id),
                    str(contract.client_id),
                    str(contract.status),
                    str(contract.remaining_amount) + " /",
                    str(contract.total_amount),
                    str(contract.creation_date.strftime("%Y-%m-%d %H:%M:%S")),
                    str(contract.commercial_contact_id),
                ]
                rows.append(row)
            options = {
                "Status": {"style": "bold magenta"},
                "Remaining Amount": {"justify": "right", "style": "bold cyan"},
                "Total Amount": {"justify": "left", "style": "cyan"},
                "Creation Date": {"justify": "left", "style": "green"},
            }
            View.table_show("CONTRACTS Table", columns, rows, options)
            if list_returns:
                return [contract.id for contract in contracts]
            else:
                View.input_return_prints("continue")

    def get_contract_id(self, contracts_ids, action=None):
        """Ask the user for a Contract ID among contracts_ids possible ids."""
        return Input.integer(f"Enter the Contract ID {action}: ", choices=contracts_ids)

    def get_contract_update_data(self, contract, clients, commercials):
        """Ask the user for contract fields to update."""
        View.menu("Contract Update Datas - " + str(self.username.capitalize()), [])
        # print("\x1B[A\x1b[2K\x1B[A")
        View.space(23)
        View.prt_info_blue(f"Updating Contract ID:\x1B[0;0m \x1B[93m{contract.id}")

        View.prt_yellow(f"Current Client ID:  \x1B[35m{contract.client_id}")
        View.prt_yellow(f"Current Status:  \x1B[36m{contract.status}")
        View.prt_yellow(f"Current Total Amount:  \x1B[36m{contract.total_amount}")
        View.prt_yellow(f"Current Remaining Amount:  \x1B[36m{contract.remaining_amount}")
        View.prt_yellow(f"Current Creation Date:  \x1B[36m{contract.creation_date.strftime("%Y-%m-%d %H:%M:%S")}")
        View.prt_yellow(f"Current Commercial Contact ID:  \x1B[36m{contract.commercial_contact_id}\n")

        View.prt_info_blue(" --- Enter new values OR leave blank to keep current value --- \x1B[33;0m\n")
        updated_data = {}

        clients_list = View.show_compact_list("Clients to choose from ", clients, "full_name")
        new_client_id = Input.integer("\n\x1B[94mNew Client ID : \x1B[93m", choices=clients_list, upd=True)
        if new_client_id:
            updated_data["client_id"] = new_client_id

        new_status = Input.signed_contract("\x1B[94mNew Status (unsigned, signed) : \x1B[93m", upd=True)
        if new_status:
            updated_data["status"] = new_status

        new_total_amount = Input.float("\x1B[94mNew Total Amount : \x1B[93m", upd=True)
        if new_total_amount is not None:
            updated_data["total_amount"] = new_total_amount

        new_remaining_amount = Input.float(
            "\x1B[94mNew Remaining Amount : \x1B[93m",
            limit=new_total_amount if new_total_amount else contract.total_amount,
            upd=True,
        )
        if new_remaining_amount is not None:
            updated_data["remaining_amount"] = new_remaining_amount

        commercials_list = View.show_compact_list("Commercials", commercials, "username")
        new_commercial_contact_id = Input.integer(
            "\n\x1B[94mNew Commercial Contact ID : \x1B[93m", commercials_list, upd=True
        )
        if new_commercial_contact_id:
            updated_data["commercial_contact_id"] = new_commercial_contact_id

        return updated_data
