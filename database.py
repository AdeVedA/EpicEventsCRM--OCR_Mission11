import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base

load_dotenv(dotenv_path=".env")
# Configuration of the connection to PostgreSql
db_url = (
    f"postgresql+psycopg2://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Creates an SQLALCHEMY engine (the "bridge" between Python and PostgreSql)
engine = create_engine(db_url)

# Create a session class to interact with the database
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """
    Creates all tables in the database from models.
    This function must be called once, during the initial creation.
    """
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables successfully created !")
    except Exception as e:
        print("Error when creating tables :", e)
