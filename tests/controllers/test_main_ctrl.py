import pytest

from controllers.main_ctrl import MainController


@pytest.fixture
def management_user(setup_users):
    """Récupère l'utilisateur avec le rôle MANAGEMENT depuis setup_users."""
    return next(user for user in setup_users if user.role.value == "MANAGEMENT")


@pytest.fixture
def commercial_user(setup_users):
    """Récupère l'utilisateur avec le rôle COMMERCIAL depuis setup_users."""
    return next(user for user in setup_users if user.role.value == "COMMERCIAL")


@pytest.fixture
def support_user(setup_users):
    """Récupère l'utilisateur avec le rôle SUPPORT depuis setup_users."""
    return next(user for user in setup_users if user.role.value == "SUPPORT")


@pytest.fixture
def mock_main_menu_view(mocker):
    """Mock la vue principale pour simuler les choix de l'utilisateur."""
    return mocker.patch("views.main_view.MainMenuView")


@pytest.fixture
def mock_user_ctrl(mocker):
    """Mock du contrôleur UserController."""
    return mocker.patch("controllers.user_ctrl.UserController")


@pytest.fixture
def mock_client_ctrl(mocker):
    """Mock du contrôleur ClientController."""
    return mocker.patch("controllers.client_ctrl.ClientController")


@pytest.fixture
def mock_event_ctrl(mocker):
    """Mock du contrôleur EventController."""
    return mocker.patch("controllers.event_ctrl.EventController")


def test_management_menu_flow(mocker, management_user):
    """Teste le menu principal pour un utilisateur MANAGEMENT."""
    # Mock de MainMenuView
    mock_main_menu_view = mocker.patch("controllers.main_ctrl.MainMenuView")
    mock_managers_menu = mock_main_menu_view.return_value.managers_menu

    # "1" (aller dans UserController), puis "0" (retour au menu principal), enfin "0" (sortir du programme)
    mock_managers_menu.side_effect = ["1", "0", "0"]

    # Mock de UserController
    mock_user_ctrl = mocker.patch("controllers.main_ctrl.UserController")

    # Initialiser le contrôleur principal
    controller = MainController(management_user)

    # Appeler la méthode principale
    controller.main()

    assert mock_managers_menu.call_count == 2

    # Vérifie que UserController est appelé une seule fois avec le bon utilisateur
    mock_user_ctrl.assert_called_once_with(management_user)

    # Vérifie que la méthode managers_collaborator_menu est appelée une fois
    mock_user_ctrl.return_value.managers_collaborator_menu.assert_called_once()


def test_commercial_menu_flow(mocker, commercial_user):
    """Teste le menu principal pour un utilisateur COMMERCIAL."""
    # Mock de MainMenuView
    mock_main_menu_view = mocker.patch("controllers.main_ctrl.MainMenuView")
    mock_commercials_menu = mock_main_menu_view.return_value.commercials_menu

    # "1" (aller dans ClientController), puis "0" (retour au menu principal), enfin "0" (sortir du programme)
    mock_commercials_menu.side_effect = ["1", "0", "0"]

    # Mock de ClientController
    mock_client_ctrl = mocker.patch("controllers.main_ctrl.ClientController")

    # Initialiser le contrôleur principal
    controller = MainController(commercial_user)

    # Appeler la méthode principale
    controller.main()

    assert mock_commercials_menu.call_count == 2

    # Vérifie que ClientController est appelé une seule fois avec le bon utilisateur
    mock_client_ctrl.assert_called_once_with(commercial_user)

    # Vérifie que la méthode commercials_client_menu est appelée une fois
    mock_client_ctrl.return_value.commercials_client_menu.assert_called_once()


def test_support_menu_flow(mocker, support_user):
    """Teste le menu principal pour un utilisateur SUPPORT."""
    # Mock de MainMenuView
    mock_main_menu_view = mocker.patch("controllers.main_ctrl.MainMenuView")
    mock_supports_menu = mock_main_menu_view.return_value.supports_menu

    # "1" (aller dans EventController), puis "0" (retour au menu principal), enfin "0" (sortir du programme)
    mock_supports_menu.side_effect = ["1", "0", "0"]

    # Mock de EventController
    mock_event_ctrl = mocker.patch("controllers.main_ctrl.EventController")

    # Initialiser le contrôleur principal
    controller = MainController(support_user)

    # Appeler la méthode principale
    controller.main()

    assert mock_supports_menu.call_count == 2

    # Vérifie que ClientController est appelé une seule fois avec le bon utilisateur
    mock_event_ctrl.assert_called_once_with(support_user)

    # Vérifie que la méthode supports_event_menu est appelée une fois
    mock_event_ctrl.return_value.supports_event_menu.assert_called_once()
