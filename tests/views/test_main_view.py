import pytest

from views.main_view import MainMenuView


@pytest.fixture
def mock_input(mocker):
    """Mock la fonction d'entrée"""
    return mocker.patch("builtins.input", return_value="1")


@pytest.fixture
def mock_view_menu(mocker):
    """Mocker la méthode View.Menu de view"""
    return mocker.patch("views.view.View.menu")


def test_managers_menu(setup_users, mock_input, mock_view_menu):
    """Teste l'affichage et l'entrée du menu des managers"""
    # Obtenir l'utilisateur manager
    manager = [user for user in setup_users if user.role.value == "MANAGEMENT"][0]

    # Créer l'instance de vue du menu principal avec le manager
    main_menu = MainMenuView(manager)

    # Appelle la méthode du menu des managers
    result = main_menu.managers_menu()

    # Vérifie si View.Menu a été appelé avec les bons arguments
    mock_view_menu.assert_called_once_with(
        f"Managers Menu -  {manager.username.capitalize()}",
        [
            "1. Collaborators management",
            "",
            "2. Contracts management",
            "",
            "3. Events management",
            "",
            "4. Clients list",
            "",
            "",
            "0. Quit",
        ],
    )

    # Vérifie si le résultat correspond à notre entrée mockée à 1
    assert result == "1"


def test_commercials_menu(setup_users, mock_input, mock_view_menu):
    """Teste l'affichage et l'entrée du menu des commerciaux"""
    # Obtenir l'utilisateur commercial
    commercial = [user for user in setup_users if user.role.value == "COMMERCIAL"][0]

    # Créer l'instance de vue du menu principal avec le commercial
    main_menu = MainMenuView(commercial)

    # Appelle la méthode du menu des commerciaux
    result = main_menu.commercials_menu()

    # Vérifie si View.Menu a été appelé avec les bons arguments
    mock_view_menu.assert_called_once_with(
        f"Commercials Menu - {commercial.username.capitalize()}",
        [
            "1. Clients management",
            "",
            "2. Contracts management",
            "",
            "3. Events management",
            "",
            "",
            "0. Quit",
        ],
    )

    # Vérifie si le résultat correspond à notre entrée mockée à 1
    assert result == "1"


def test_supports_menu(setup_users, mock_input, mock_view_menu):
    """Teste l'affichage et l'entrée du menu des supports"""
    # Obtenir l'utilisateur support
    support = [user for user in setup_users if user.role.value == "SUPPORT"][0]

    # Créer l'instance d'affichage du menu principal avec le support
    main_menu = MainMenuView(support)

    # Appelle la méthode du menu des supports
    result = main_menu.supports_menu()

    # Vérifie si View.Menu a été appelé avec les bons arguments
    mock_view_menu.assert_called_once_with(
        f"Supports Menu - {support.username.capitalize()}",
        [
            "1. Events management",
            "",
            "2. Contracts list",
            "",
            "3. Clients list",
            "",
            "",
            "0. Quit",
        ],
    )

    # Vérifie si le résultat correspond à notre entrée mockée à 1
    assert result == "1"


@pytest.mark.parametrize("menu_choice", ["0", "2", "3", "4"])
def test_managers_menu_different_choices(setup_users, mock_view_menu, mocker, menu_choice):
    """Test the managers menu with different input choices"""
    # Mocker l'entrée avec les différents paramètres de menu_choice
    mocker.patch("builtins.input", return_value=menu_choice)

    # Obtenir l'utilisateur manager
    manager = [user for user in setup_users if user.role.value == "MANAGEMENT"][0]

    # Créer l'instance de vue du menu principal avec le manager
    main_menu = MainMenuView(manager)
    result = main_menu.managers_menu()

    # Vérifie si le résultat correspond à notre entrée paramètrée
    assert result == menu_choice


@pytest.mark.parametrize("menu_choice", ["0", "2", "3"])
def test_commercials_menu_different_choices(setup_users, mock_view_menu, mocker, menu_choice):
    """Test the commercials menu with different input choices"""
    # Mocker l'entrée avec les différents paramètres de menu_choice
    mocker.patch("builtins.input", return_value=menu_choice)

    # Obtenir l'utilisateur commercial
    commercial = [user for user in setup_users if user.role.value == "COMMERCIAL"][0]

    # Créer l'instance de vue du menu principal avec le commercial
    main_menu = MainMenuView(commercial)
    result = main_menu.commercials_menu()

    # Vérifie si le résultat correspond à notre entrée paramètrée
    assert result == menu_choice


@pytest.mark.parametrize("menu_choice", ["0", "2", "3"])
def test_supports_menu_different_choices(setup_users, mock_view_menu, mocker, menu_choice):
    """Test the supports menu with different input choices"""
    # Mocker l'entrée avec les différents paramètres de menu_choice
    mocker.patch("builtins.input", return_value=menu_choice)

    # Obtenir l'utilisateur support
    support = [user for user in setup_users if user.role.value == "SUPPORT"][0]

    # Créer l'instance de vue du menu principal avec le support
    main_menu = MainMenuView(support)
    result = main_menu.supports_menu()

    # Vérifie si le résultat correspond à notre entrée paramètrée
    assert result == menu_choice
