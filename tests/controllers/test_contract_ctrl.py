from datetime import datetime

import pytest

from controllers.client_ctrl import ClientController
from controllers.contract_ctrl import ContractController
from controllers.user_ctrl import UserController
from models.models import Client, Contract, User
from views.contract_view import ContractView


@pytest.fixture
def contract_controller(db_session, setup_users):
    """Fixture pour initialiser le ContractController avec un utilisateur manager."""
    manager_user = db_session.query(User).filter_by(role="MANAGEMENT").first()
    return ContractController(manager_user)


@pytest.fixture
def setup_test_contract(db_session, setup_users, setup_clients):
    """Créer un contrat de test."""
    commercial = db_session.query(User).filter_by(role="COMMERCIAL").first()
    client = db_session.query(Client).first()

    contract = Contract(
        client_id=client.id,
        commercial_contact_id=commercial.id,
        total_amount=1000.0,
        remaining_amount=500.0,
        status="unsigned",
        creation_date=datetime.now(),
    )
    db_session.add(contract)
    db_session.commit()
    return contract


def test_create_contract(db_session, contract_controller, setup_clients, setup_users, mocker, ret_prt_mock):
    """Teste la création d'un contrat."""
    # Récupérer les objets par leurs attributs uniques
    commercial = db_session.query(User).filter_by(role="COMMERCIAL").first()
    client = db_session.query(Client).filter_by(full_name="Client A").first()

    mock_data = {
        "client_id": client.id,
        "commercial_contact_id": commercial.id,
        "total_amount": 1000.0,
        "remaining_amount": 500.0,
        "status": "unsigned",
    }

    mocker.patch.object(ClientController, "get_clients", return_value=[client])
    mocker.patch.object(UserController, "get_commercials", return_value=[commercial])
    mocker.patch.object(ContractView, "get_contract_creation_data", return_value=mock_data)

    contract_controller.create_contract(session=db_session)

    # Vérification
    contract = db_session.query(Contract).first()
    assert contract is not None
    assert contract.client_id == client.id
    assert contract.commercial_contact_id == commercial.id
    assert contract.total_amount == 1000.0
    assert contract.remaining_amount == 500.0
    assert contract.status == "unsigned"


def test_list_contracts_display(db_session, contract_controller, setup_test_contract, mocker):
    """Test de l'affichage de tous les contrats."""
    # Mock de la méthode show_contracts
    mock_show_contracts = mocker.patch.object(ContractView, "show_contracts")

    # Appel de la méthode
    contract_controller.list_contracts(session=db_session)

    # Vérification
    all_contracts = db_session.query(Contract).all()
    mock_show_contracts.assert_called_once_with(all_contracts)
    assert len(all_contracts) > 0


def test_list_contracts_with_ids(db_session, contract_controller, setup_test_contract, mocker):
    """Test de la liste des contrats en retournant leurs IDs."""
    # Mock de la méthode show_contracts
    mock_show_contracts = mocker.patch.object(ContractView, "show_contracts", return_value=[setup_test_contract.id])

    # Appel de la méthode avec l'option `list_returns=True`
    contract_ids = contract_controller.list_contracts(list_returns=True, session=db_session)

    # Vérification
    all_contracts = db_session.query(Contract).all()
    mock_show_contracts.assert_called_once_with(all_contracts, True)
    assert contract_ids == [setup_test_contract.id]
    assert len(contract_ids) > 0


def test_update_contract(db_session, contract_controller, setup_test_contract, mocker, ret_prt_mock):
    """Teste la mise à jour d'un contrat."""
    # Mock des méthodes
    mocker.patch.object(contract_controller, "list_contracts", return_value=[setup_test_contract.id])
    mocker.patch.object(ContractView, "get_contract_id", return_value=setup_test_contract.id)
    mocker.patch.object(ClientController, "get_clients", return_value=[Client(id=1)])
    mocker.patch.object(UserController, "get_commercials", return_value=[User(id=2)])

    updated_data = {"total_amount": 2000.0, "remaining_amount": 1000.0, "status": "signed"}
    mocker.patch.object(ContractView, "get_contract_update_data", return_value=updated_data)

    # Test de la mise à jour
    contract_controller.update_contract(session=db_session)

    # Vérification
    updated_contract = db_session.query(Contract).filter_by(id=setup_test_contract.id).first()
    assert updated_contract.total_amount == 2000.0
    assert updated_contract.remaining_amount == 1000.0
    assert updated_contract.status == "signed"


def test_list_unsigned_contracts(db_session, contract_controller, setup_test_contract, mocker, ret_prt_mock):
    """Teste la liste des contrats non signés."""
    # Appel de la méthode
    contract_controller.list_unsigned_contracts(session=db_session)

    # Vérification que la méthode s'exécute sans erreur
    unsigned_contracts = db_session.query(Contract).filter(Contract.status == "unsigned").all()
    assert len(unsigned_contracts) > 0
    assert all(contract.status == "unsigned" for contract in unsigned_contracts)


def test_list_unpaid_contracts(db_session, contract_controller, setup_test_contract, mocker, ret_prt_mock):
    """Teste la liste des contrats impayés."""
    # Ajout d'un contrat payé pour le test
    paid_contract = Contract(
        client_id=setup_test_contract.client_id,
        commercial_contact_id=setup_test_contract.commercial_contact_id,
        total_amount=1000.0,
        remaining_amount=0.0,
        status="signed",
    )
    db_session.add(paid_contract)
    db_session.commit()

    # Appel de la méthode
    contract_controller.list_unpaid_contracts(session=db_session)

    # Vérification
    unpaid_contracts = [c for c in db_session.query(Contract).all() if c.remaining_amount > 0]
    assert len(unpaid_contracts) > 0
    assert all(contract.remaining_amount > 0 for contract in unpaid_contracts)


def test_list_signed_contracts(db_session, contract_controller, setup_test_contract, mocker, ret_prt_mock):
    """Teste la liste des contrats signés."""
    # Modifier le contrat de test pour qu'il soit signé
    setup_test_contract.status = "signed"
    db_session.commit()

    # Ajouter un contrat non signé pour s'assurer qu'il n'est pas dans les résultats
    unsigned_contract = Contract(
        client_id=setup_test_contract.client_id,
        commercial_contact_id=setup_test_contract.commercial_contact_id,
        total_amount=1000.0,
        remaining_amount=1000.0,
        status="unsigned",
    )
    db_session.add(unsigned_contract)
    db_session.commit()

    # Appel de la méthode
    contract_controller.list_signed_contracts(session=db_session)

    # Vérification
    signed_contracts = db_session.query(Contract).filter(Contract.status == "signed").all()

    assert len(signed_contracts) > 0
    assert all(contract.status == "signed" for contract in signed_contracts)
