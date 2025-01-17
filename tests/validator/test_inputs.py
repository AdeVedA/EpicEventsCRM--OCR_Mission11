from datetime import datetime

import pytest

from validator.inputs import Input


@pytest.fixture
def mock_input(mocker):
    """Fixture pour simuler l'entrée utilisateur"""
    return mocker.patch("validator.inputs.Input._input")


@pytest.fixture
def mock_error_alert(mocker):
    """Fixture pour simuler les alertes d'erreur"""
    return mocker.patch("views.error_view.ErrorView.alert")


class TestInput:
    def test_integer_valid(self, mock_input):
        """Teste la conversion d'une entrée en nombre entier valide"""
        mock_input.return_value = "42"
        assert Input.integer("Enter number: ") == 42

    def test_integer_invalid(self, mock_input, mock_error_alert):
        """Teste le traitement d'une entrée invalide pour un nombre entier"""
        mock_input.side_effect = ["abc", "42"]
        assert Input.integer("Enter number: ") == 42
        mock_error_alert.assert_called_once()

    def test_integer_with_choices(self, mock_input, mock_error_alert):
        """Teste la validation des choix pour un nombre entier"""
        mock_input.side_effect = ["4", "2"]
        assert Input.integer("Choose: ", choices=[1, 2, 3]) == 2
        mock_error_alert.assert_called_once()

    def test_float_limit_exceeded(self, mock_input, mock_error_alert):
        """Teste le respect de la limite supérieure pour un nombre décimal"""
        mock_input.side_effect = ["60.0", "42.5"]
        assert Input.float("Enter float: ", limit=50.0) == 42.5
        mock_error_alert.assert_called_once()

    def test_string_name_validation(self, mock_input, mock_error_alert):
        """Teste la validation du format pour un nom"""
        mock_input.side_effect = ["John123", "John Doe"]
        assert Input.string_name("Enter name: ") == "John Doe"
        mock_error_alert.assert_called_once()

    def test_date_format(self, mock_input, mock_error_alert):
        """Teste la validation du format de date standard"""
        mock_input.side_effect = ["invalid", "29/12/2025 17:30:59"]
        assert Input.date("Enter date: ") == "29/12/2025 17:30:59"
        mock_error_alert.assert_called_once()

    def test_event_date_format(self, mock_input):
        """Teste la validation du format de date d'événement"""
        mock_input.return_value = "4 Jun 2023 @ 1PM"
        assert Input.event_date("Enter event date: ") == "4 Jun 2023 @ 1PM"

    def test_date_default_now(self, mock_input, mocker):
        """Teste la valeur par défaut de la date actuelle"""
        mock_input.return_value = ""
        mock_datetime = mocker.patch("validator.inputs.datetime")
        mock_datetime.today.return_value = datetime(2025, 12, 29, 17, 30, 59)
        assert Input.date_default_to_now("Enter date: ") == "29/12/2025 17:30:59"

    def test_email_format(self, mock_input, mock_error_alert):
        """Teste la validation du format d'email"""
        mock_input.side_effect = ["invalid", "test@example.com"]
        assert Input.email("Enter email: ") == "test@example.com"
        mock_error_alert.assert_called_once()

    def test_phone_number_format(self, mock_input):
        """Teste la validation du format de numéro de téléphone"""
        mock_input.return_value = "06 68 15 24 64"
        assert Input.phone_number("Enter phone: ") == "06 68 15 24 64"

    def test_company_name_format(self, mock_input):
        """Teste la validation du format de nom d'entreprise"""
        mock_input.return_value = "Tech-Co Ltd."
        assert Input.company_name("Enter company: ") == "Tech-Co Ltd."

    def test_role_validation(self, mock_input, mock_error_alert):
        """Teste la validation des rôles autorisés"""
        mock_input.side_effect = ["INVALID", "MANAGEMENT"]
        assert Input.role("Enter role: ") == "MANAGEMENT"
        mock_error_alert.assert_called_once()

    def test_signed_contract_validation(self, mock_input):
        """Teste la validation du statut de signature du contrat"""
        mock_input.return_value = "signed"
        assert Input.signed_contract("Enter status: ") == "signed"

    def test_empty_update_mode(self, mock_input):
        """Teste le comportement en mode mise à jour avec une entrée vide"""
        mock_input.return_value = ""
        assert Input.string("Enter value: ", upd=True) is None
