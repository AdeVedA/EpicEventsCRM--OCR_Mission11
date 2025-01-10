from validator.inputs import Input
from views.view import View


class EventView(View):
    def __init__(self, user):
        self.user = user
        self.username = user.username

    # MANAGEMENTS EVENT MENU
    def managers_event_show(self):
        """Shows the managers event menu"""
        username = self.username
        header = "Events Menu -  " + str(username.capitalize())
        menu_options = [
            "1. List events",
            "2. List events without support",
            "3. Associate a support to an event",
            "",
            "0. Back",
        ]
        View.menu(header, menu_options)
        choice = input()
        return choice

    # COMMERCIALS EVENT MENU
    def commercials_event_show(self):
        """Shows the commercials event menu"""
        username = self.username
        header = "Events Menu -  " + str(username.capitalize())
        menu_options = [
            "1. List events",
            "2. Create event for a signed contract",
            "",
            "0. Back",
        ]
        View.menu(header, menu_options)
        choice = input()
        return choice

    # SUPPORTS EVENT MENU
    def supports_event_show(self):
        """Shows the supports event menu"""
        username = self.username
        header = "Events Menu -  " + str(username.capitalize())
        menu_options = [
            "1. List events",
            "2. List my own events",
            "3. Update my own events",
            "",
            "0. Back",
        ]
        View.menu(header, menu_options)
        choice = input()
        return choice

    def show_events(self, events, list_returns=None):
        """displays events table (and return list of events if list_returns=True)"""
        if not events:
            View.input_return_prints("no_event")
        else:
            View.menu("events' List - " + str(self.username.capitalize()), [])
            columns = [
                "ID",
                "Title",
                "Support ID",
                "Start Date",
                "End Date",
                "Location",
                "Attendees",
                "Notes",
                "Contract ID",
            ]
            rows = []
            for event in events:
                row = [
                    str(event.id),
                    str(event.title),
                    str(event.support_contact_id),
                    str(event.start_date),
                    str(event.end_date),
                    str(event.location),
                    str(event.attendees),
                    str(event.notes),
                    str(event.contract_id),
                ]
                rows.append(row)
            options = {
                "Title": {"justify": "left", "style": "bold magenta"},
                "Start Date": {"justify": "left", "style": "green"},
                "End Date": {"justify": "left", "style": "green"},
                "Location": {"style": "bold cyan"},
                "Attendees": {"style": "turquoise2"},
                "Notes": {"style": "aquamarine1"},
            }
            View.table_show("EVENTS Table", columns, rows, options)
            if list_returns:
                return [event.id for event in events]
            else:
                View.input_return_prints("continue")

    def get_event_creation_data(self, contract_id):
        """Ask the user for the data needed to create an event"""
        View.menu("Event Creation - " + str(self.username.capitalize()), [])
        print("\n\n\x1b[1A\x1b[2K\x1B[35mPlease enter event informations")
        return {
            "title": Input.anything("Title : \x1B[33m"),
            "contract_id": contract_id,
            "start_date": Input.event_date("Start date (e.g.: 20 Jun 1969 @ 5PM) : \x1B[33m"),
            "end_date": Input.event_date("End date : \x1B[33m"),
            "location": Input.string_name("Location : \x1B[33m"),
            "attendees": Input.integer("Attendees : \x1B[33m"),
            "notes": Input.anything("Notes : \x1B[33m"),
        }

    def get_event_id(self, events_ids, action=None):
        """Ask the user for an Event ID among events_ids possible ids."""
        return Input.integer(f"Enter the Event ID {action}: ", events_ids)

    def confirm_support_change(self, support):
        """confirm the intention to change the support collaborator for an event"""
        answer = (
            input(
                (
                    f"Are you sure you want to change the support \x1B[35m{support.username} "
                    f"(id {support.id}) \x1B[36mto another for the event ? \x1B[33m(y/n) : "
                )
            )
            .strip()
            .lower()
        )
        return answer == "y"

    def get_support_id_for_event(self, supports):
        """Identify the support collaborator to associate to an event"""
        supports_list = View.show_compact_list("Supports", supports, "username")
        support_contact_id = Input.integer("\nSelect Support Contact ID from the list: \x1B[33m", supports_list)
        return support_contact_id

    def get_event_update_data(self, event, contracts, supports):
        """Ask the user for event fields to update."""
        View.menu("Event Update Datas - " + str(self.username.capitalize()), [])
        # print("\x1B[A\x1b[2K\x1B[A")
        View.space(23)
        View.prt_info_blue(f"Updating Event ID:\x1B[0;0m \x1B[93m{event.id}")

        View.prt_yellow(f"Current Title: \x1B[35m{event.title}")
        View.prt_yellow(f"Current Contract ID: \x1B[35m{event.contract_id}")
        View.prt_yellow(f"Current Start date: \x1B[36m{event.start_date}")
        View.prt_yellow(f"Current End date: \x1B[36m{event.end_date}")
        View.prt_yellow(f"Current Support Contact ID: \x1B[35m{event.support_contact_id}")
        View.prt_yellow(f"Current Location: \x1B[36m{event.location}")
        View.prt_yellow(f"Current Attendees: \x1B[36m{event.attendees}")
        View.prt_yellow(f"Current Notes: \x1B[36m{event.notes}\n")

        View.prt_info_blue(" --- Enter new values OR leave blank to keep current value --- \x1B[33;0m\n")
        updated_data = {}

        new_title = Input.anything("\x1B[94mNew Title : \x1B[93m", upd=True)
        if new_title:
            updated_data["title"] = new_title

        contracts_list = View.show_compact_list("Contracts to choose from ", contracts, "full_name")
        new_contract_id = Input.integer("\x1B[94mNew Contract ID : \x1B[93m", choices=contracts_list, upd=True)
        if new_contract_id:
            updated_data["contract_id"] = new_contract_id

        new_start_date = Input.event_date("\x1B[94mNew Start date : \x1B[93m", upd=True)
        if new_start_date:
            updated_data["start_date"] = new_start_date

        new_end_date = Input.event_date("\x1B[94mNew End date : \x1B[93m", upd=True)
        if new_end_date:
            updated_data["end_date"] = new_end_date

        supports_list = View.show_compact_list("Supports to choose from ", supports, "full_name")
        new_support_id = Input.integer("\x1B[94mNew Contract ID : \x1B[93m", choices=supports_list, upd=True)
        if new_support_id:
            updated_data["support_contact_id"] = new_support_id

        new_location = Input.string_name("\x1B[94mNew Location : \x1B[93m", upd=True)
        if new_location:
            updated_data["location"] = new_location

        new_attendees = Input.integer("\x1B[94mNew Attendees : \x1B[93m", upd=True)
        if new_attendees is not None:
            updated_data["attendees"] = new_attendees

        new_notes = Input.anything("\x1B[94mNew Notes : \x1B[93m", upd=True)
        if new_notes:
            updated_data["notes"] = new_notes

        return updated_data
