from controllers.event_ctrl import EventController
from models.models import Event, User


def test_list_events(db_session, setup_events, setup_users, mocker):
    """Test la liste des événements."""
    commercial = db_session.query(User).filter_by(role="COMMERCIAL").first()
    controller = EventController(commercial)

    # Mock la vue pour simuler le retour de la liste d'IDs
    mock_show_events = mocker.patch.object(
        controller.view, "show_events", return_value=[event.id for event in setup_events]
    )

    # avec list_returns=True
    events_ids = controller.list_events(list_returns=True)
    assert isinstance(events_ids, list)
    assert len(events_ids) == 2
    mock_show_events.assert_called_once()

    # Reset le mock
    mock_show_events.reset_mock()

    # sans list_returns
    result = controller.list_events()
    assert result is None
    mock_show_events.assert_called_once()


def test_list_events_without_support(db_session, setup_events, setup_users, mocker):
    """Test la liste des événements sans support assigné."""
    manager = db_session.query(User).filter_by(role="MANAGEMENT").first()
    EventController(manager)
    events = db_session.query(Event).filter(Event.support_contact_id.is_(None)).all()
    assert len(events) == 1


def test_list_my_events(db_session, setup_events, setup_users):
    """Test la liste des événements d'un support."""
    support = db_session.query(User).filter_by(role="SUPPORT").first()
    EventController(support)
    events = db_session.query(Event).filter_by(support_contact_id=support.id).all()
    assert len(events) == 1


def test_commercials_event_menu(mocker, setup_users):
    """Test le menu des événements pour les commerciaux."""
    mocker.patch("views.view.View.input_return_prints")
    commercial = setup_users[1]  # Commercial user
    controller = EventController(commercial)

    # Mock la vue pour simuler différents choix de menu
    mock_show = mocker.patch.object(controller.view, "commercials_event_show")
    mock_list = mocker.patch.object(controller, "list_events")
    mock_create = mocker.patch.object(controller, "create_event")

    # Liste des événements
    mock_show.side_effect = ["1", "0"]  # Simule choix 1 puis sortie
    controller.commercials_event_menu()
    mock_list.assert_called_once()

    # Réinitialiser les mocks
    mock_list.reset_mock()
    mock_create.reset_mock()

    # Créer un événement
    mock_show.side_effect = ["2", "0"]  # Simule choix 2 puis sortie
    controller.commercials_event_menu()
    mock_create.assert_called_once()

    # sortie directe
    mock_list.reset_mock()
    mock_create.reset_mock()
    mock_show.side_effect = ["0"]  # Simule sortie immédiate
    controller.commercials_event_menu()
    assert mock_list.call_count == 0
    assert mock_create.call_count == 0

    # choix invalide
    mock_show.side_effect = ["invalid", "0"]  # Simule choix invalide puis sortie
    controller.commercials_event_menu()
    assert mock_list.call_count == 0
    assert mock_create.call_count == 0


def test_create_event(db_session, setup_contracts, setup_clients, setup_users, mocker):
    """Test la création d'un événement par un commercial."""
    mocker.patch("views.view.View.input_return_prints")
    # Récupérer un commercial et un contrat signé
    commercial = db_session.query(User).filter_by(role="COMMERCIAL").first()
    signed_contract = next(contract for contract in setup_contracts if contract.status == "signed")

    # Créer le controller avec le commercial
    event_controller = EventController(commercial)

    # Préparer les données de test
    event_data = {
        "title": "Event infundibuliforme",
        "contract_id": signed_contract.id,
        "start_date": "04 Jun 2023 @ 01PM",
        "end_date": "05 Jun 2023 @ 01PM",
        "location": "Marseille",
        "attendees": 40,
        "notes": "notes entonnoirs",
    }

    # Mock des méthodes
    mocker.patch("controllers.contract_ctrl.ContractController.list_signed_contracts", return_value=[signed_contract])
    mocker.patch("controllers.contract_ctrl.ContractController.choose_contract_id", return_value=signed_contract.id)
    mocker.patch.object(event_controller.view, "get_event_creation_data", return_value=event_data)

    # Action
    event_controller.create_event(session=db_session)

    # Assertions
    created_event = db_session.query(Event).filter_by(title="Event infundibuliforme").first()

    assert created_event is not None
    assert created_event.title == event_data["title"]
    assert created_event.contract_id == event_data["contract_id"]
    assert created_event.start_date == event_data["start_date"]
    assert created_event.end_date == event_data["end_date"]
    assert created_event.location == event_data["location"]
    assert created_event.attendees == event_data["attendees"]
    assert created_event.notes == event_data["notes"]


def test_managers_event_menu(mocker, setup_users):
    """Test le menu des événements pour les managers."""
    mocker.patch("views.view.View.input_return_prints")
    manager = setup_users[0]  # Manager user
    controller = EventController(manager)

    # Mock des méthodes
    mock_show = mocker.patch.object(controller.view, "managers_event_show")
    mock_list = mocker.patch.object(controller, "list_events")
    mock_list_without = mocker.patch.object(controller, "list_events_without_support")
    mock_associate = mocker.patch.object(controller, "associate_event_support")

    # Liste des événements
    mock_show.side_effect = ["1", "0"]
    controller.managers_event_menu()
    mock_list.assert_called_once()

    # Liste des événements sans support
    mock_show.side_effect = ["2", "0"]
    controller.managers_event_menu()
    mock_list_without.assert_called_once()

    # Associer un support
    mock_show.side_effect = ["3", "0"]
    controller.managers_event_menu()
    mock_associate.assert_called_once()

    # Réinitialiser les mocks
    mock_list.reset_mock()
    mock_list_without.reset_mock()
    mock_associate.reset_mock()

    # Test choix invalide
    mock_show.side_effect = ["invalid", "0"]
    controller.managers_event_menu()
    assert not mock_list.called
    assert not mock_list_without.called
    assert not mock_associate.called


def test_supports_event_menu(mocker, setup_users):
    """Test le menu des événements pour les supports."""
    mocker.patch("views.view.View.input_return_prints")
    support = setup_users[2]  # Support user
    controller = EventController(support)

    # Mock des méthodes
    mock_show = mocker.patch.object(controller.view, "supports_event_show")
    mock_list = mocker.patch.object(controller, "list_events")
    mock_list_my = mocker.patch.object(controller, "list_my_events")
    mock_update = mocker.patch.object(controller, "update_own_events")

    # Liste des événements
    mock_show.side_effect = ["1", "0"]
    controller.supports_event_menu()
    mock_list.assert_called_once()

    # Liste de mes événements
    mock_show.side_effect = ["2", "0"]
    controller.supports_event_menu()
    mock_list_my.assert_called_once()

    # Mettre à jour mes événements
    mock_show.side_effect = ["3", "0"]
    controller.supports_event_menu()
    mock_update.assert_called_once()

    # Réinitialiser les mocks
    mock_list.reset_mock()
    mock_list_my.reset_mock()
    mock_update.reset_mock()

    # Test choix invalide
    mock_show.side_effect = ["invalid", "0"]
    controller.supports_event_menu()
    assert not mock_list.called
    assert not mock_list_my.called
    assert not mock_update.called


def test_associate_event_support(db_session, setup_events, setup_users, mocker):
    """Test l'association d'un support à un événement."""
    mocker.patch("views.view.View.input_return_prints")
    manager = db_session.query(User).filter_by(role="MANAGEMENT").first()
    support = db_session.query(User).filter_by(role="SUPPORT").first()
    event = setup_events[1]  # Événement sans support
    controller = EventController(manager)

    # Mock des méthodes
    mocker.patch.object(controller, "list_events", return_value=[event.id])
    mocker.patch.object(controller.view, "get_event_id", return_value=event.id)
    mocker.patch.object(controller.view, "confirm_support_change", return_value=True)
    mocker.patch.object(controller.view, "get_support_id_for_event", return_value=support.id)

    # Action
    controller.associate_event_support(session=db_session)

    # Vérification
    updated_event = db_session.query(Event).filter_by(id=event.id).first()
    assert updated_event.support_contact_id == support.id


def test_update_own_events(db_session, setup_events, setup_users, setup_contracts, mocker):
    """Test la mise à jour d'un événement par un support."""
    mocker.patch("views.view.View.input_return_prints")
    support = db_session.query(User).filter_by(role="SUPPORT").first()
    event = next(event for event in setup_events if event.support_contact_id == support.id)
    controller = EventController(support)

    # Données de mise à jour
    updated_data = {
        "title": "Updated Event Title",
        "location": "Updated Location",
        "attendees": 100,
        "notes": "Updated notes",
    }

    # Mock des méthodes
    mocker.patch.object(controller, "list_events", return_value=[event.id])
    mocker.patch.object(controller.view, "get_event_id", return_value=event.id)
    mocker.patch.object(controller.view, "get_event_update_data", return_value=updated_data)

    # Action
    controller.update_own_events(session=db_session)

    # Vérification
    updated_event = db_session.query(Event).filter_by(id=event.id).first()
    assert updated_event.title == updated_data["title"]
    assert updated_event.location == updated_data["location"]
    assert updated_event.attendees == updated_data["attendees"]
    assert updated_event.notes == updated_data["notes"]


def test_update_own_events_forbidden(db_session, setup_events, setup_users, mocker):
    """Test la tentative de mise à jour d'un événement non assigné au support."""
    mocker.patch("views.view.View.input_return_prints")
    support = db_session.query(User).filter_by(role="SUPPORT").first()
    event = next(event for event in setup_events if event.support_contact_id != support.id)
    controller = EventController(support)

    # Mock des méthodes
    mocker.patch.object(controller, "list_events", return_value=[event.id])
    mocker.patch.object(controller.view, "get_event_id", return_value=event.id)

    # Action
    result = controller.update_own_events(session=db_session)

    # Vérification
    assert result is None
