import pytest

from models.models import User
from views.event_view import EventView


@pytest.fixture
def commercial_user(setup_users, db_session):
    """Crée un utilisateur avec le rôle COMMERCIAL."""
    commercial = db_session.query(User).filter_by(role="COMMERCIAL").first()
    return commercial


@pytest.fixture
def event_view(commercial_user):
    """Instancie EventView avec un utilisateur commercial."""
    return EventView(commercial_user)


def test_managers_event_show(event_view, mock_input):
    """Teste la sélection d'événements pour les managers."""
    mock_input.return_value = "1"
    assert event_view.managers_event_show() == "1"


def test_commercials_event_show(event_view, mock_input):
    """Teste la sélection d'événements pour les commerciaux."""
    mock_input.return_value = "2"
    assert event_view.commercials_event_show() == "2"


def test_supports_event_show(event_view, mock_input):
    """Teste la sélection d'événements pour le support."""
    mock_input.return_value = "3"
    assert event_view.supports_event_show() == "3"


def test_show_events(event_view, setup_events):
    """Teste que `show_events` retourne une liste d'IDs."""
    events_ids = event_view.show_events(setup_events, list_returns=True)
    assert isinstance(events_ids, list)
    assert len(events_ids) > 0


def test_show_events_empty(event_view, mocker, ret_prt_mock):
    """Teste que `show_events` retourne None si la liste d'événements est vide."""
    result = event_view.show_events([], list_returns=True)
    assert result is None


def test_get_event_creation_data(event_view, mock_input):
    """Teste la collecte des données pour la création d'un événement."""
    inputs = ["Test Event", "20 Jun 2024 @ 2PM", "20 Jun 2024 @ 5PM", "Paris", "50", "Test notes"]
    mock_input.side_effect = inputs

    result = event_view.get_event_creation_data(contract_id=1)
    assert result["title"] == "Test Event"
    assert result["contract_id"] == 1
    assert result["location"] == "Paris"
    assert result["attendees"] == 50
    assert result["notes"] == "Test notes"


def test_get_event_id(event_view, mock_input):
    """Teste la sélection d'un ID d'événement."""
    mock_input.return_value = "1"
    result = event_view.get_event_id([1, 2, 3])
    assert result == 1


def test_confirm_support_change(event_view, mock_input, setup_users, db_session):
    """Teste la confirmation de changement de support."""
    support = db_session.query(User).filter_by(role="SUPPORT").first()

    mock_input.return_value = "y"
    assert event_view.confirm_support_change(support) is True

    mock_input.return_value = "n"
    assert event_view.confirm_support_change(support) is False


def test_get_support_id_for_event(event_view, mock_input, setup_users):
    """Teste la sélection d'un support pour un événement."""
    mock_input.return_value = "1"
    supports = [u for u in setup_users if u.role == "SUPPORT"]
    result = event_view.get_support_id_for_event(supports)
    assert result == 1


def test_get_event_update_data(event_view, mock_input, setup_events, setup_contracts, setup_users, mocker):
    """Teste la collecte des données pour la mise à jour d'un événement."""
    mocker.patch("views.view.View.show_compact_list", return_value=[1])

    inputs = ["Updated Event", "1", "20 Jul 2024 @ 2PM", "20 Jul 2024 @ 5PM", "1", "Lyon", "75", "Updated notes"]
    mock_input.side_effect = inputs
    event = setup_events[0]
    supports = [u for u in setup_users if u.role == "SUPPORT"]

    result = event_view.get_event_update_data(event, setup_contracts, supports)
    assert result["title"] == "Updated Event"
    assert result["location"] == "Lyon"
    assert result["attendees"] == 75
    assert result["notes"] == "Updated notes"


def test_get_event_update_data_empty(event_view, mock_input, setup_events, setup_contracts, setup_users, mocker):
    """Teste le cas où les données de mise à jour sont vides."""
    mocker.patch("views.view.View.show_compact_list", return_value=[1])
    mock_input.side_effect = [""] * 8

    event = setup_events[0]
    supports = [u for u in setup_users if u.role == "SUPPORT"]
    result = event_view.get_event_update_data(event, setup_contracts, supports)

    assert len(result) == 0
