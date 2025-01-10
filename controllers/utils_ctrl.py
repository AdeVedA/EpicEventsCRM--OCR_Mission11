import os
from functools import wraps  # Allows decorated functions' docstrings to be preserved
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from views.error_view import ErrorView
from views.view import View

# Database configuration
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def with_session(func):
    """
    Decorator to automatically manage SQLAlchemy sessions,
    or use an existing session if provided.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if 'session' is already provided in kwargs
        if "session" in kwargs and kwargs["session"]:
            return func(*args, **kwargs)

        # Otherwise, create a new session
        with Session() as session:
            kwargs["session"] = session
            try:
                return func(*args, **kwargs)
            except Exception as e:
                session.rollback()
                ErrorView().alert(f"Database error: {e}")
                View.press_key()

    return wrapper
