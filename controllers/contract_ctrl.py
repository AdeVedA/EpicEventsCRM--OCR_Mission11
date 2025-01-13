from controllers.client_ctrl import ClientController
from controllers.user_ctrl import UserController
from controllers.utils_ctrl import with_session
from models.models import Contract
from views.contract_view import ContractView
from views.view import View


class ContractController:
    def __init__(self, user):
        self.user = user
        self.view = ContractView(user)

    def managers_contract_menu(self):
        while True:
            choice = self.view.managers_contract_show()
            match choice:
                case "1":
                    # List contracts
                    self.list_contracts()
                case "2":
                    # Create contracts
                    self.create_contract()
                case "3":
                    # Update contract
                    self.update_contract()
                case "0":
                    # Exit the menu
                    break
                case _:
                    View.input_return_prints("choice_error")

    def commercials_contract_menu(self):
        while True:
            choice = self.view.commercials_contract_show()
            match choice:
                case "1":
                    # List contracts
                    self.list_contracts()
                case "2":
                    # Update my client's contract
                    self.update_contract(own=True)
                case "3":
                    # Display unsigned contracts
                    self.list_unsigned_contracts()
                case "4":
                    # Display unpaid contracts
                    self.list_unpaid_contracts()
                case "0":
                    # Exit the menu
                    break
                case _:
                    View.input_return_prints("choice_error")

    @with_session
    def create_contract(self, session=None):
        """Create a new contract in the database."""
        clients = ClientController(self.user).get_clients()
        if not clients:
            View.input_return_prints("no_client")
            return
        commercials = UserController(self.user).get_commercials()
        if not commercials:
            View.input_return_prints("no_user")
            return
        data = self.view.get_contract_creation_data(clients, commercials)
        contract = Contract(
            client_id=data["client_id"],
            commercial_contact_id=data["commercial_contact_id"],
            total_amount=data["total_amount"],
            remaining_amount=data["remaining_amount"],
            status=data["status"],
        )
        session.add(contract)
        session.commit()
        # Reloads the contract object to include relations (to name the customer, here)
        session.refresh(contract)
        View.input_return_prints("contract_saved", contract.id, contract.client.full_name)

    @with_session
    def list_contracts(self, list_returns=None, session=None):
        """List all contracts."""
        contracts = session.query(Contract).all()
        if list_returns:
            return self.view.show_contracts(contracts, list_returns)
        else:
            self.view.show_contracts(contracts)

    @with_session
    def update_contract(self, own=False, session=None):
        """Update a contract."""
        contracts_ids = self.list_contracts(list_returns=True)
        if not contracts_ids:
            return
        contract_id = self.view.get_contract_id(contracts_ids, action="to update ")
        clients = ClientController(self.user).get_clients()
        commercials = UserController(self.user).get_commercials()
        contract = session.query(Contract).filter_by(id=contract_id).first()
        if own and contract.commercial_contact_id != self.user.id:
            View.input_return_prints("forbidden")
            return
        if not contract:
            View.input_return_prints("no_contract")
            return
        updated_data = self.view.get_contract_update_data(contract, clients, commercials)
        for attr, value in updated_data.items():
            setattr(contract, attr, value)
        session.commit()
        session.refresh(contract)
        View.input_return_prints("contract_saved", contract.id, contract.client.full_name)

    @with_session
    def list_unsigned_contracts(self, list_returns=None, session=None):
        """List all unsigned contracts."""
        unsigned_contracts = session.query(Contract).filter(Contract.status == "unsigned").all()
        self.view.show_contracts(unsigned_contracts, list_returns)

    @with_session
    def list_unpaid_contracts(self, list_returns=None, session=None):
        """List all contracts."""
        contracts = session.query(Contract).all()
        for contract in contracts:
            if contract.remaining_amount == 0:
                contracts.remove(contract)
        self.view.show_contracts(contracts, list_returns)

    @with_session
    def list_signed_contracts(self, list_returns=True, session=None):
        """List all signed contracts."""
        signed_contracts = (
            session.query(Contract)
            .filter(Contract.status == "signed", Contract.commercial_contact_id == self.user.id)
            .all()
        )
        return self.view.show_contracts(signed_contracts, list_returns)

    def choose_contract_id(self, signed_contracts_ids):
        """choose a contract id for an event creation"""
        return self.view.get_contract_id(signed_contracts_ids, action="of the event ")

    @with_session
    def get_signed_contracts(self, session=None):
        """Retrieve all contracts."""
        return session.query(Contract).filter(Contract.status == "signed").all()
