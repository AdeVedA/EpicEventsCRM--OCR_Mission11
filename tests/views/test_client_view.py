import pytest

from views.client_view import ClientView


@pytest.fixture
def mock_user(mocker):
    """Fixture pour mocker un user."""
    return mocker.Mock(id=1, username="test_user")


@pytest.fixture
def client_view(mock_user):
    """Fixture pour initialiser la ClientView."""
    return ClientView(mock_user)


def test_commercials_client_show(client_view, mocker):
    """Teste la méthode d'affichage de menu pour les commerciaux."""
    mock_menu = mocker.patch("views.view.View.menu")
    mock_input = mocker.patch("builtins.input", return_value="1")

    choice = client_view.commercials_client_show()

    mock_menu.assert_called_once()
    mock_input.assert_called_once()
    assert choice == "1"


def test_get_client_creation_data(client_view, mocker):
    """Teste la méthode d'entrée des données pour la création d'un client."""
    # Mocker les méthodes d'entrée
    mocker.patch("validator.inputs.Input.string_name", side_effect=["Arthur Saizmat"])
    mocker.patch("validator.inputs.Input.email", return_value="art.sai@zmat.com")
    mocker.patch("validator.inputs.Input.phone_number", return_value="0687654321")
    mocker.patch("validator.inputs.Input.company_name", return_value="Saiz Inc.")

    # Appele la méthode
    data = client_view.get_client_creation_data()

    # Tests
    assert data == {
        "full_name": "Arthur Saizmat",
        "email": "art.sai@zmat.com",
        "phone": "0687654321",
        "company_name": "Saiz Inc.",
    }


def test_show_clients(client_view, mocker):
    """Teste la méthode d'afficvhage des clients."""
    mock_view_table = mocker.patch("views.view.View.table_show")
    mock_view_continue = mocker.patch("views.view.View.input_return_prints")

    # Mocker les clients
    mock_client = mocker.Mock(
        id=1,
        full_name="Arthur Saizmat",
        email="art.sai@zmat.com",
        phone="0687654321",
        company_name="Saiz Inc.",
        commercial_contact_id=1,
        creation_date=mocker.Mock(strftime=lambda fmt: "2025-01-01 12:00:00"),
        last_update_date=mocker.Mock(strftime=lambda fmt: "2025-01-02 12:00:00"),
    )

    client_view.show_clients([mock_client])

    # tests
    mock_view_table.assert_called_once()
    mock_view_continue.assert_called_once_with("continue")


def test_get_client_update_data_no_changes(client_view, setup_clients, mocker):
    """Teste la mise à jour d'un client sans aucun changement."""
    # Récupérer un client existant
    client = setup_clients[0]

    # Mocker les nouvelles valeurs saisies par l'utilisateur
    mocker.patch("validator.inputs.Input.string_name", return_value=None)  # Pas de changement
    mocker.patch("validator.inputs.Input.email", return_value=None)  # Pas de changement
    mocker.patch("validator.inputs.Input.phone_number", return_value=None)  # Pas de changement
    mocker.patch("validator.inputs.Input.company_name", return_value=None)  # Pas de changement
    mocker.patch("validator.inputs.Input.integer", return_value=None)  # Pas de changement
    mock_show_compact_list = mocker.patch(
        "views.view.View.show_compact_list", return_value=[client.commercial_contact_id]
    )

    # Appeler la méthode
    updated_data = client_view.get_client_update_data(
        client, [{"id": client.commercial_contact_id, "username": "commercial_1"}]
    )

    # Tests
    assert updated_data == {}  # Aucun champ modifié
    mock_show_compact_list.assert_called_once_with(
        "Commercials", [{"id": client.commercial_contact_id, "username": "commercial_1"}], "username"
    )


def test_get_client_update_data_with_changes(client_view, setup_clients, mocker):
    """Teste la mise à jour complète d'un client avec tous les champs modifiés."""
    # Récupérer un client existant
    client = setup_clients[0]

    # Mocker les nouvelles valeurs saisies par l'utilisateur
    mocker.patch("validator.inputs.Input.string_name", return_value="Nouveau Nom")
    mocker.patch("validator.inputs.Input.email", return_value="nouveau.email@test.com")
    mocker.patch("validator.inputs.Input.phone_number", return_value="0712345678")
    mocker.patch("validator.inputs.Input.company_name", return_value="Nouvelle Entreprise")
    mocker.patch("validator.inputs.Input.integer", return_value=2)  # Nouveau commercial_contact_id
    mock_show_compact_list = mocker.patch(
        "views.view.View.show_compact_list", return_value=[client.commercial_contact_id, 2]
    )

    # Appeler la méthode
    updated_data = client_view.get_client_update_data(
        client,
        [
            {"id": client.commercial_contact_id, "username": "commercial_1"},
            {"id": 2, "username": "commercial_2"},
        ],
    )

    # Tests
    assert updated_data == {
        "full_name": "Nouveau Nom",
        "email": "nouveau.email@test.com",
        "phone": "0712345678",
        "company_name": "Nouvelle Entreprise",
        "commercial_contact_id": 2,
    }
    mock_show_compact_list.assert_called_once_with(
        "Commercials",
        [
            {"id": client.commercial_contact_id, "username": "commercial_1"},
            {"id": 2, "username": "commercial_2"},
        ],
        "username",
    )


def test_get_client_update_data_partial_changes(client_view, setup_clients, mocker):
    """Teste la mise à jour partielle d'un client avec certains champs modifiés."""
    # Récupérer un client existant
    client = setup_clients[1]

    # Mocker les nouvelles valeurs saisies par l'utilisateur
    mocker.patch("validator.inputs.Input.string_name", return_value=None)  # Pas de changement
    mocker.patch("validator.inputs.Input.email", return_value="nouveau.email@test.com")  # Email modifié
    mocker.patch("validator.inputs.Input.phone_number", return_value=None)  # Pas de changement
    mocker.patch("validator.inputs.Input.company_name", return_value="Nouvelle Entreprise")  # Nom modifié
    mocker.patch("validator.inputs.Input.integer", return_value=None)  # Pas de changement
    mock_show_compact_list = mocker.patch(
        "views.view.View.show_compact_list", return_value=[client.commercial_contact_id]
    )

    # Appeler la méthode
    updated_data = client_view.get_client_update_data(
        client,
        [
            {"id": client.commercial_contact_id, "username": "commercial_1"},
        ],
    )

    # Tests
    assert updated_data == {
        "email": "nouveau.email@test.com",
        "company_name": "Nouvelle Entreprise",
    }
    mock_show_compact_list.assert_called_once_with(
        "Commercials",
        [{"id": client.commercial_contact_id, "username": "commercial_1"}],
        "username",
    )
