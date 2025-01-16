import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base

# Charger les variables d'environnement
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

# Configuration de la base de données de test
TEST_DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Créer le moteur SQLAlchemy
engine = create_engine(TEST_DATABASE_URL)
Session = sessionmaker(bind=engine)


@pytest.fixture(scope="session")
def db_engine():
    """Initialisation de la base de données pour les tests."""
    Base.metadata.create_all(engine)  # Créer les tables
    yield engine
    Base.metadata.drop_all(engine)  # Supprimer les tables après les tests


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Fournir une session pour chaque test."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def setup_users(db_session):
    """Créer des utilisateurs de base pour les tests."""
    from models.models import User

    # Supprimer les utilisateurs existants
    db_session.query(User).delete()

    # Réinitialiser la séquence d'ID
    # db_session.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1;")

    # Créer de nouveaux utilisateurs
    manager = User(username="testmanager", password=User.hash_password("securepassword"), role="MANAGEMENT")
    commercial = User(username="testcommercial", password=User.hash_password("securepassword"), role="COMMERCIAL")
    support = User(username="testsupport", password=User.hash_password("securepassword"), role="SUPPORT")

    # Ajouter et valider les utilisateurs
    db_session.add_all([manager, commercial, support])
    db_session.commit()

    # Validation
    users = db_session.query(User).all()
    print(f"Utilisateurs créés : {[user.username for user in users]} , ids {[user.id for user in users]}")
    return users


@pytest.fixture(scope="function")
def setup_clients(db_session, setup_users):
    """Créer des clients pour les tests."""
    from models.models import Client, User

    # Supprimer les clients existants
    db_session.query(Client).delete()

    # Récupérer l'ID du commercial de manière dynamique
    commercial = db_session.query(User).filter_by(role="COMMERCIAL").first()

    # Créer de nouveaux clients
    client1 = Client(
        full_name="Client A",
        email="clienta@test.com",
        phone="123456789",
        company_name="la boite A",
        commercial_contact_id=commercial.id,
    )
    client2 = Client(
        full_name="Client B",
        email="clientb@test.com",
        phone="987654321",
        company_name="la boite B",
        commercial_contact_id=commercial.id,
    )

    # Ajouter et valider les clients
    db_session.add_all([client1, client2])
    db_session.commit()

    return db_session.query(Client).all()


@pytest.fixture(scope="function")
def setup_contracts(db_session, setup_clients, setup_users):
    """Créer des contrats pour les tests."""
    from models.models import Client, Contract, User

    # Supprimer les contrats existants
    db_session.query(Contract).delete()

    # Récupérer les utilisateurs et les clients
    commercial = db_session.query(User).filter_by(role="COMMERCIAL").first()
    client = db_session.query(Client).first()

    # Créer des contrats
    contract1 = Contract(
        client_id=client.id,
        commercial_contact_id=commercial.id,
        total_amount=3000.0,
        remaining_amount=1500.0,
        status="unsigned",
    )
    contract2 = Contract(
        client_id=client.id,
        commercial_contact_id=commercial.id,
        total_amount=2000.0,
        remaining_amount=0.0,
        status="signed",
    )

    # Ajouter et valider les contrats
    db_session.add_all([contract1, contract2])
    db_session.commit()

    return db_session.query(Contract).all()


@pytest.fixture(scope="function")
def setup_events(db_session, setup_contracts, setup_users):
    """Créer des événements pour les tests."""
    from datetime import datetime

    from models.models import Event, User

    # Supprimer les événements existants
    db_session.query(Event).delete()

    # Récupérer le premier contrat et le support
    contract = setup_contracts[0]
    support = db_session.query(User).filter_by(role="SUPPORT").first()

    # Créer des événements
    event1 = Event(
        title="Test Event 1",
        contract_id=contract.id,
        start_date=datetime(2024, 6, 1, 14, 0),
        end_date=datetime(2024, 6, 1, 17, 0),
        location="Paris",
        attendees=50,
        notes="Test notes 1",
        support_contact_id=support.id,
    )

    event2 = Event(
        title="Test Event 2",
        contract_id=contract.id,
        start_date=datetime(2024, 7, 1, 10, 0),
        end_date=datetime(2024, 7, 1, 16, 0),
        location="Lyon",
        attendees=30,
        notes="Test notes 2",
    )

    # Ajouter et valider les événements
    db_session.add_all([event1, event2])
    db_session.commit()

    return db_session.query(Event).all()
