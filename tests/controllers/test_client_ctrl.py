import pytest

from controllers.client_ctrl import ClientController
from models.models import Client
from views.client_view import ClientView


@pytest.fixture
def client_controller(db_session, setup_users):
    """Fixture pour initialiser le ClientController avec un utilisateur commercial."""
    from models.models import User

    # Récupérer un utilisateur commercial existant
    commercial_user = db_session.query(User).filter_by(role="COMMERCIAL").first()
    return ClientController(commercial_user)


def test_create_client(client_controller, mocker, db_session):
    """Teste la méthode de création d'un client create_client."""
    mocker.patch("views.view.View.input_return_prints")
    # Mock des données de la vue
    mock_view_data = {
        "full_name": "Arthur Saizmat",
        "email": "art.sai@zmat.com",
        "phone": "0687654321",
        "company_name": "Saiz Inc.",
    }
    mocker.patch.object(ClientView, "get_client_creation_data", return_value=mock_view_data)

    # Appeler la méthode
    client_controller.create_client(session=db_session)

    # Vérifications en base
    client = db_session.query(Client).filter_by(full_name="Arthur Saizmat").first()
    assert client is not None
    assert client.email == "art.sai@zmat.com"
    assert client.phone == "0687654321"
    assert client.company_name == "Saiz Inc."


def test_list_clients(client_controller, mocker, db_session):
    """Teste la méthode list_clients."""
    # Ajouter un client dans la base
    client = Client(
        full_name="Arthur Saizmat",
        email="art.sai@zmat.com",
        phone="0687654321",
        company_name="Saiz Inc.",
        commercial_contact_id=client_controller.user.id,
    )
    db_session.add(client)
    db_session.commit()

    # Mock de la méthode de vue
    mock_show_clients = mocker.patch.object(ClientView, "show_clients")

    # Appeler la méthode
    client_controller.list_clients(session=db_session)

    # Vérification
    mock_show_clients.assert_called_once_with([client])


def test_update_client(db_session, setup_users, client_controller, mocker):
    """Teste la méthode update_client."""
    mocker.patch("views.view.View.input_return_prints")
    # Mocker la Session pour qu'elle retourne la db_session de test
    session_mock = mocker.patch("controllers.utils_ctrl.Session")
    session_mock.return_value.__enter__.return_value = db_session

    # Ajouter un client dans la base
    client = Client(
        full_name="Arthur Saizmat",
        email="art.sai@zmat.com",
        phone="0687654321",
        company_name="Saiz Inc.",
        commercial_contact_id=client_controller.user.id,
    )
    db_session.add(client)
    db_session.commit()

    # Mock de la méthode list_clients pour retourner une liste d'IDs
    mocker.patch.object(client_controller, "list_clients", return_value=[client.id])

    # Mock de la méthode get_client_id pour sélectionner ce client
    mocker.patch.object(ClientView, "get_client_id", return_value=client.id)

    # Mock de get_client_update_data pour fournir les nouvelles données
    mocker.patch.object(
        ClientView,
        "get_client_update_data",
        return_value={"full_name": "Falbala Saizmat", "email": "Falbala.Sai@zmat.com"},
    )

    # Appeler la méthode update_client
    client_controller.update_client()

    print(f"client: {client.full_name}, {client.email}, {client_controller.user.id}")
    print(f"client's commercial_contact_id: {client.commercial_contact_id}")

    # Vérifications en base
    updated_client = db_session.query(Client).filter_by(id=client.id).first()

    print(f"Updated client: {updated_client.full_name}, {updated_client.email}")
    assert updated_client.full_name == "Falbala Saizmat"
    assert updated_client.email == "Falbala.Sai@zmat.com"
    assert updated_client.phone == "0687654321"
    assert updated_client.company_name == "Saiz Inc."
