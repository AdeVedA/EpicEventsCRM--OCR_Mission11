from controllers.contract_ctrl import ContractController
from controllers.user_ctrl import UserController
from controllers.utils_ctrl import with_session
from models.models import Event, User
from views.event_view import EventView
from views.view import View


class EventController:
    def __init__(self, user):
        self.user = user
        self.view = EventView(user)

    def managers_event_menu(self):
        while True:
            choice = self.view.managers_event_show()
            match choice:
                case "1":
                    # List events
                    self.list_events()
                case "2":
                    # List events without support
                    self.list_events_without_support()
                case "3":
                    # Associate a support to an event
                    self.associate_event_support()
                case "0":
                    # Exit the menu
                    break
                case _:
                    View.input_return_prints("choice_error")

    def commercials_event_menu(self):
        while True:
            choice = self.view.commercials_event_show()
            match choice:
                case "1":
                    # List events
                    self.list_events()
                case "2":
                    # Create event for a signed contract
                    self.create_event()
                case "0":
                    # Exit the menu
                    break
                case _:
                    View.input_return_prints("choice_error")

    def supports_event_menu(self):
        while True:
            choice = self.view.supports_event_show()
            match choice:
                case "1":
                    # List events
                    self.list_events()
                case "2":
                    # List my own events
                    self.list_my_events()
                case "3":
                    # Update my own events
                    self.update_own_events()
                case "0":
                    # Exit the menu
                    break
                case _:
                    View.input_return_prints("choice_error")

    @with_session
    def create_event(self, session=None):
        """Create a new event in the database."""
        contractctrl = ContractController(self.user)
        signed_contracts_ids = contractctrl.list_signed_contracts()
        if signed_contracts_ids:
            contract_id = contractctrl.choose_contract_id(signed_contracts_ids)
        else:
            return
        if contract_id:
            data = self.view.get_event_creation_data(contract_id)
        if data:
            event = Event(
                title=data["title"],
                contract_id=data["contract_id"],
                start_date=data["start_date"],
                end_date=data["end_date"],
                location=data["location"],
                attendees=data["attendees"],
                notes=data["notes"],
            )
            session.add(event)
            session.commit()
            View.input_return_prints("event_saved", event.id, event.title)

    @with_session
    def list_events(self, list_returns=None, session=None):
        """List all events."""
        events = session.query(Event).all()
        if list_returns:
            return self.view.show_events(events, list_returns)
        else:
            self.view.show_events(events, list_returns)

    @with_session
    def list_events_without_support(self, session=None):
        """List all events without support assigned."""
        events_without_support = session.query(Event).filter(Event.support_contact_id.is_(None)).all()
        self.view.show_events(events_without_support)

    @with_session
    def list_my_events(self, session=None):
        """List all events without support assigned."""
        events_self_support = session.query(Event).where(Event.support_contact_id == self.user.id).all()
        self.view.show_events(events_self_support)

    @with_session
    def associate_event_support(self, session=None):
        """associate a support collaborator to an event (manager's functionality)"""
        events_ids = self.list_events(list_returns=True)
        if not events_ids:
            return
        event_id = self.view.get_event_id(events_ids, action="to associate a support to ")
        # try avant requête base... except
        event = session.query(Event).filter_by(id=event_id).first()
        try:
            support = session.query(User).filter_by(id=event.support_contact_id).first()
            if support:
                if not self.view.confirm_support_change(support):
                    return View.input_return_prints("event_support_saved", "cancel")
            supports = UserController.get_supports()
            event.support_contact_id = self.view.get_support_id_for_event(supports)
            session.commit()
            session.refresh(event)
            View.input_return_prints("event_support_saved", "ok", event.title, event.support_contact.username)
        except ValueError as e:
            print(f"Value Error : {e}")
        except Exception as e:
            print(f"Exception : {e}")

    @with_session
    def update_own_events(self, session=None):
        """Update a support's assigned own event."""
        events_ids = self.list_events(list_returns=True)
        if not events_ids:
            return
        event_id = self.view.get_event_id(events_ids, action="to update ")
        event = session.query(Event).filter_by(id=event_id).first()
        contracts = ContractController(self.user).get_signed_contracts()
        supports = UserController(self.user).get_supports()
        if event.support_contact_id != self.user.id:
            View.input_return_prints("forbidden")
            return
        if not event:
            View.input_return_prints("no_event")
            return
        updated_data = self.view.get_event_update_data(event, contracts, supports)
        for attr, value in updated_data.items():
            setattr(event, attr, value)
        session.commit()
        session.refresh(event)
        View.input_return_prints("event_saved", event.id, event.title)
