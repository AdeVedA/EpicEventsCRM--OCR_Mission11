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
    Base.metadata.create_all(engine)  # Créer les tables une seule fois
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

    # Créer de nouveaux utilisateurs
    manager = User(username="testmanager", password=User.hash_password("securepassword"), role="MANAGEMENT")
    commercial = User(username="testcommercial", password=User.hash_password("securepassword"), role="COMMERCIAL")
    support = User(username="testsupport", password=User.hash_password("securepassword"), role="SUPPORT")

    # Ajouter et valider les utilisateurs
    db_session.add_all([manager, commercial, support])
    db_session.commit()

    # Validation
    users = db_session.query(User).all()
    print(f"Utilisateurs créés : {[user.username for user in users]}")
    return users


@pytest.fixture(scope="function")
def setup_clients(db_session):
    """Créer des clients pour les tests."""
    from models.models import Client

    # Supprimer les clients existants
    db_session.query(Client).delete()

    # Créer de nouveaux clients
    client1 = Client(
        full_name="Client A",
        email="clienta@test.com",
        phone="123456789",
        company_name="la boite A",
        commercial_contact_id=2,
    )
    client2 = Client(
        full_name="Client B",
        email="clientb@test.com",
        phone="987654321",
        company_name="la boite B",
        commercial_contact_id=2,
    )

    # Ajouter et valider les clients
    db_session.add_all([client1, client2])
    db_session.commit()

    return db_session.query(Client).all()


@pytest.fixture(scope="function")
def setup_contracts(db_session):
    """Créer des contrats pour les tests."""
    from models.models import Contract, User

    # Supprimer les contrats existants
    db_session.query(Contract).delete()

    # Récupérer les utilisateurs et les clients
    commercial = next(user for user in db_session.query(User).all() if user.role == "COMMERCIAL")
    client = setup_clients[0]

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
