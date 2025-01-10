from controllers.utils_ctrl import with_session
from models.models import User
from views.user_view import UserView
from views.view import View


class UserController:
    def __init__(self, user):
        self.user = user
        self.view = UserView(user)

    def managers_collaborator_menu(self):
        while True:
            choice = self.view.managers_collaborator_show()
            match choice:
                case "1":
                    # List collaborators
                    self.list_collaborators()
                case "2":
                    # Create collaborator
                    self.create_collaborator()
                case "3":
                    # Update collaborator
                    self.update_user()
                case "4":
                    # Delete collaborator
                    self.delete_user()
                case "0":
                    # Exit the menu
                    break
                case _:
                    View.input_return_prints("choice_error")

    @with_session
    def list_collaborators(self, update=False, session=None):
        """List all collaborators."""
        collaborators = session.query(User).all()
        if update:
            collabs_ids = self.view.show_collaborators(collaborators, update)
            return collabs_ids
        else:
            self.view.show_collaborators(collaborators, update)

    @with_session
    def create_collaborator(self, session=None):
        """Create a new collaborator in the database."""
        data = self.view.get_collaborator_creation_data()
        hashed_password = User.hash_password(data["password"])
        collab = User(
            username=data["username"],
            password=hashed_password,
            role=data["role"],
        )
        session.add(collab)
        session.commit()
        View.input_return_prints("collab_saved", collab.id, collab.username, collab.role)

    @with_session
    def update_user(self, session=None):
        """Update a collaborator."""
        collabs_ids = self.list_collaborators(update=True)
        user_id = self.view.get_user_id(collabs_ids, action="to update")
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            View.input_return_prints("no_user")
            return

        updated_data = self.view.get_user_update_data(user)
        if "password" in updated_data:
            updated_data["password"] = User.hash_password(updated_data["password"])
        for attr, value in updated_data.items():
            setattr(user, attr, value)
        session.commit()
        View.input_return_prints("collab_saved", user.id, user.username, user.role)

    @with_session
    def delete_user(self, session=None):
        """Delete a collaborator"""
        collabs_ids = self.list_collaborators(update=True)
        user_id = self.view.get_user_id(collabs_ids, action="to delete")
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            View.input_return_prints("no_user")
            return
        if self.view.confirm_user_delete(user):
            try:
                session.delete(user)
                session.commit()
                View.input_return_prints("user_delete", "ok", user.username)
            except Exception as e:
                session.rollback()
                View.input_return_prints("user_delete", "except", {e})
        else:
            View.input_return_prints("user_delete", "cancel")

    @with_session
    def get_users(self, session=None):
        """Retrieve all collaborators."""
        return session.query(User).all()

    @with_session
    def get_commercials(self, session=None):
        """Retrieve all commercials."""
        return session.query(User).filter_by(role="COMMERCIAL").all()

    @staticmethod
    @with_session
    def get_supports(session=None):
        """Retrieve all supports."""
        return session.query(User).filter_by(role="SUPPORT").all()
