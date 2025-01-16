import pytest

from models.models import User
from views.contract_view import ContractView


@pytest.fixture
def contract_view(db_session, setup_users):
    """Fixture pour initialiser ContractView avec un utilisateur manager."""
    manager = db_session.query(User).filter_by(role="MANAGEMENT").first()
    return ContractView(manager)


def test_show_contracts(contract_view, setup_contracts):
    """Test de l'affichage des contrats."""
    contracts = setup_contracts
    result = contract_view.show_contracts(contracts, list_returns=True)
    print(f"setup contract_id : {setup_contracts[0].id}, result : {result}")
    assert setup_contracts[0].id in result


def test_get_contract_id(contract_view, setup_contracts, mocker):
    """Test de la récupération de l'ID du contrat."""
    target_contract = setup_contracts[0]

    mocker.patch("validator.inputs.Input.integer", return_value=target_contract.id)

    result = contract_view.get_contract_id([c.id for c in setup_contracts], "test")
    assert result == target_contract.id


def test_get_contract_creation_data(contract_view, db_session, setup_clients, setup_users, mocker):
    """Test de la récupération des données de création de contrat."""
    client = setup_clients[0]
    commercial = db_session.query(User).filter_by(role="COMMERCIAL").first()

    mocker.patch("validator.inputs.Input.integer", side_effect=[client.id, commercial.id])
    mocker.patch("validator.inputs.Input.float", side_effect=[1000.0, 500.0])
    mocker.patch("validator.inputs.Input.signed_contract", return_value="unsigned")

    result = contract_view.get_contract_creation_data(setup_clients, [commercial])

    assert result == {
        "client_id": client.id,
        "commercial_contact_id": commercial.id,
        "total_amount": 1000.0,
        "remaining_amount": 500.0,
        "status": "unsigned",
    }


def test_get_contract_update_data(contract_view, db_session, setup_clients, setup_contracts, mocker):
    """Test de la récupération des données de mise à jour de contrat."""
    clients = setup_clients
    commercial = [db_session.query(User).filter_by(role="COMMERCIAL").first()]

    mocker.patch("validator.inputs.Input.integer", return_value=None)
    mocker.patch("validator.inputs.Input.float", side_effect=[2000.0, 1000.0])
    mocker.patch("validator.inputs.Input.signed_contract", return_value="signed")

    result1 = contract_view.get_contract_update_data(setup_contracts[0], clients, commercial)

    assert result1 == {"total_amount": 2000.0, "remaining_amount": 1000.0, "status": "signed"}
