from controllers.user_ctrl import UserController
from controllers.utils_ctrl import with_session
from models.models import Client
from views.client_view import ClientView
from views.view import View


class ClientController:
    def __init__(self, user):
        self.user = user
        self.view = ClientView(user)

    def commercials_client_menu(self):
        while True:
            choice = self.view.commercials_client_show()
            match choice:
                case "1":
                    # Creates a client
                    self.create_client()
                case "2":
                    # Update clients
                    self.update_client()
                case "3":
                    # Lists clients
                    self.list_clients()
                case "0":
                    # Exit the menu
                    break
                case _:
                    View.input_return_prints("choice_error")

    @with_session
    def create_client(self, session=None):
        """Create a new client in the database."""
        data = self.view.get_client_creation_data()
        client = Client(
            full_name=data["full_name"],
            email=data["email"],
            phone=data["phone"],
            company_name=data["company_name"],
            commercial_contact_id=self.user.id,
        )
        session.add(client)
        session.commit()
        View.input_return_prints("client_saved", client.full_name)

    @with_session
    def list_clients(self, list_returns=False, session=None):
        """List all clients."""
        clients = session.query(Client).all()
        if list_returns:
            return self.view.show_clients(clients, list_returns)
        else:
            self.view.show_clients(clients)

    @with_session
    def get_clients(self, session=None):
        """Retrieve all clients."""
        return session.query(Client).all()

    @with_session
    def update_client(self, session=None):
        """Update a client."""
        clients_ids = self.list_clients(list_returns=True)
        if not clients_ids:
            return
        client_id = self.view.get_client_id(clients_ids, action="to update ")
        client = session.query(Client).filter_by(id=client_id).first()
        if not client:
            View.input_return_prints("no_client")
            return
        commercials = UserController(self.user).get_commercials()
        if not commercials:
            return
        if client.commercial_contact_id != self.user.id:
            View.input_return_prints("forbidden")
            return
        updated_data = self.view.get_client_update_data(client, commercials)
        if updated_data:
            for attr, value in updated_data.items():
                setattr(client, attr, value)
            session.commit()
            session.refresh(client)
            View.input_return_prints("client_saved", client.full_name)
        else:
            return
