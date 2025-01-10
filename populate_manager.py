import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import User, UserDepartment


def populate_users(user_to_create):
    """
    Crée des utilisateurs prédéfinis en base.
    """
    # Database configuration
    load_dotenv(dotenv_path=".env")
    DATABASE_URL = (
        f"postgresql+psycopg2://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for user_data in user_to_create:
            # Check if the user already exists
            existing_user = session.query(User).filter_by(username=user_data["username"]).first()
            if existing_user:
                print(f"The user '{user_data['username']}' already exists. Ignored.")
                continue

            # Convert the role to enum UserDepartment
            try:
                role_enum = UserDepartment[user_data["role"]]
            except KeyError:
                print(f"The role '{user_data['role']}' is not valid.")
                continue

            # Create a new user
            hashed_password = User.hash_password(user_data["password"])
            new_user = User(
                username=user_data["username"],
                password=hashed_password,
                role=role_enum,
            )
            session.add(new_user)
            print(f"Addition of the user '{user_data['username']}' with the role '{user_data['role']}'.")

        # Validate changes
        session.commit()
        print("All users have been successfully added.")
    except Exception as e:
        session.rollback()
        print(f"Error when adding users : {e}")
    finally:
        session.close()
