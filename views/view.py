import os
import shutil
import time

from rich.console import Console
from rich.table import Table


class View:
    # Select Graphic Rendition subset
    OFF = "\x1B[0;0m"
    WHITE = "\x1B[97m"
    GREEN = "\x1B[92m"
    YELLOW = "\x1B[93m"
    RED = "\x1B[91m"
    CYAN = "\x1B[96m"
    BLUE = "\x1B[94m"
    MAGENTA = "\x1B[95m"
    BOLD = "\x1B[1m"
    UNDERLINE = "\x1B[4m"
    # mix with background FONTCOLOR_BACKGROUND
    WHITE_RED = "\x1B[97;41m"
    YELLOW_RED = "\x1B[93;41m"
    BLACK_GREEN = "\x1B[90;42m"
    YELLOW_BLUE = "\x1B[93;44m"
    RED_CYAN = "\x1B[91;46m"
    RED_YELLOW = "\x1B[91;43m"

    @staticmethod
    def prt_underline(text):
        print(f"{View.BOLD}{View.UNDERLINE}{text}{View.OFF}")

    @staticmethod
    def prt_magenta(text):
        print(f"{View.MAGENTA}{View.BOLD}{text}{View.OFF}")

    @staticmethod
    def prt_blue(text):
        print(f"{View.BLUE}{View.BOLD}{text}{View.OFF}")

    @staticmethod
    def prt_blue_no_carriage_return(text):
        print(f"{View.BLUE}{View.BOLD}{text}{View.OFF}", end="")

    @staticmethod
    def prt_cyan(text):
        print(f"{View.CYAN}{View.BOLD}{text}{View.OFF}")

    @staticmethod
    def prt_green(text):
        print(f"{View.GREEN}{View.BOLD}{text}{View.OFF}")

    @staticmethod
    def prt_yellow(text):
        print(f"{View.YELLOW}{View.BOLD}{text}{View.OFF}")

    @staticmethod
    def prt_red(text):
        print(f"{View.RED}{View.BOLD}{text}{View.OFF}")

    @staticmethod
    def prt_warn_red(text):
        print(f"{View.WHITE_RED}{View.BOLD}{text}{View.OFF}")

    @staticmethod
    def prt_warn_yred(text):
        """print yellow font on red background"""
        print(f"{View.YELLOW_RED}{View.BOLD}{text}{View.OFF}")

    @staticmethod
    def prt_info_green(text):
        print(f"{View.BLACK_GREEN}{View.BOLD}{text}{View.OFF}")

    @staticmethod
    def prt_info_blue(text):
        print(f"{View.YELLOW_BLUE}{View.BOLD}{text}{View.OFF}")

    @staticmethod
    def prt_info_cyan(text):
        print(f"{View.RED_CYAN}{View.BOLD}{text}{View.OFF}")

    @staticmethod
    def prt_info_yellow(text):
        print(f"{View.RED_YELLOW}{View.BOLD}{text}{View.OFF}")

    @staticmethod
    def color_arg(arg):
        """Formate un argument avec une couleur cyan + gras"""
        return f"{View.MAGENTA}{View.BOLD}{arg}{View.OFF}"

    @staticmethod
    def press_key():
        """wait for user 'enter' key press"""
        input(f"{View.YELLOW}{View.BOLD}Press the key 'Enter' to continue{View.OFF}")

    @staticmethod
    def space(nbr):
        "print a passed number of spaces without carriage return"
        spaces = nbr * " "
        print(f"{View.OFF}{spaces}", end="")

    @staticmethod
    def erase_line(nbr=1):
        "print a passed number of spaces without carriage return"
        cursor_up = "\x1b[1A"
        erase_line = "\x1b[2K"
        print(f"{(cursor_up + erase_line) * nbr + cursor_up}")

    @staticmethod
    def input_return_prints(message, *args, **kwargs):
        """allows to display messages to the user in return for his inputs
        or for backups notifications...
        Args:
            message : the "case" to reference the message
            *args & **kwargs : Optional arguments for custom messages
        """
        spc = " "

        while True:
            match message:
                case "continue":
                    View.space(17)
                    View.press_key()
                    View.erase_line()
                    return
                case "choice_error":
                    View.space(10)
                    View.prt_warn_yred("❌ Please choose one of the available options ")
                    View.space(17)
                    View.press_key()
                    View.erase_line(2)
                    return
                case "forbidden":
                    View.space(13)
                    View.prt_warn_yred("❌ you are not allowed to modify this data ")
                    View.space(17)
                    View.press_key()
                    View.erase_line(2)
                    return
                case "passwords_not_match":
                    View.space(21)
                    View.prt_warn_yred("❌ Passwords do not match ")
                    View.space(17)
                    View.press_key()
                    View.erase_line(2)
                    return
                case "collab_saved":
                    View.prt_green(
                        (
                            f"\n✅ ---> {View.color_arg(args[1])}{View.GREEN}, your collaborator "
                            f"(id {View.color_arg(args[0])}{View.GREEN}), from the "
                            f"'{View.color_arg(str(args[2].value).lower())}{View.GREEN}' department, has been saved !"
                        )
                    )
                    View.space(17)
                    View.press_key()
                    return
                case "user_delete":
                    if args[0] == "cancel":
                        View.space(22)
                        View.prt_warn_yred("🚫 Cancelled suppression ")
                        View.space(17)
                        View.press_key()
                        View.erase_line(2)
                    elif args[0] == "except":
                        View.space(16)
                        View.prt_warn_yred(f"❌ Error during suppression : {View.color_arg(args[1])}")
                        View.space(17)
                        View.press_key()
                        View.erase_line(2)
                    elif args[0] == "ok":
                        View.prt_green(f"{spc*16}✅ user successfully deleted : {View.color_arg(args[1])}")
                        View.space(17)
                        View.press_key()
                        View.erase_line(2)
                    return
                case "no_user":
                    View.space(24)
                    View.prt_warn_yred("❌ User not found ! ")
                    View.space(17)
                    View.press_key()
                    View.erase_line(2)
                    return
                case "client_saved":
                    View.prt_green(f"{View.GREEN}{spc*14}✅ Client successfully saved : {View.color_arg(args[0])}")
                    View.space(17)
                    View.press_key()
                    View.erase_line(2)
                    return
                case "no_client":
                    View.space(10)
                    View.prt_warn_yred("❌ No clients. Please first register a client ")
                    View.space(17)
                    View.press_key()
                    View.erase_line(2)
                    return
                case "no_contract":
                    View.space(24)
                    View.prt_warn_yred("❌ No contract found ! ")
                    View.space(17)
                    View.press_key()
                    View.erase_line(2)
                    return
                case "contract_saved":
                    View.prt_green(
                        (
                            f"{spc*6}✅ Contract successfully saved with ID n° {View.color_arg(args[0])}"
                            f"{View.GREEN} for client {View.color_arg(args[1])}"
                        )
                    )
                    View.space(17)
                    View.press_key()
                    View.erase_line(2)
                    return
                case "no_event":
                    View.space(24)
                    View.prt_warn_yred("❌ No event found ! ")
                    View.space(17)
                    View.press_key()
                    View.erase_line(2)
                    return
                case "event_select":
                    View.prt_yellow(f"{spc*26}✅ the event '{kwargs['name']}' has been selected")
                    time.sleep(2)
                    View.erase_line(2)
                    return
                case "event_saved":
                    View.prt_green(
                        (
                            f"{spc*6}✅ Event successfully saved with title {View.color_arg(args[1])} "
                            f"{View.GREEN}and ID n°{View.color_arg(args[0])}"
                        )
                    )
                    View.space(17)
                    View.press_key()
                    View.erase_line(2)
                    return
                case "event_support_saved":
                    if args[0] == "cancel":
                        View.space(21)
                        View.prt_warn_yred("🚫 Cancelled modification ")
                        View.space(17)
                        View.press_key()
                        View.erase_line(2)
                    elif args[0] == "ok":
                        View.prt_green(
                            (
                                f"{spc*8}✅ Support {View.color_arg(args[2])}{View.GREEN} successfully assigned "
                                f"to event {View.color_arg(args[1])}"
                            )
                        )
                        View.space(17)
                        View.press_key()
                        View.erase_line(2)
                    return
                case "bienvenue":
                    View.prt_magenta(f"\n{spc*2}🌟✨  Welcome to the relationship manager with your clients ! ✨🌟\n")
                    View.space(18)
                    View.press_key()
                    return
                case "quit":
                    View.prt_magenta("\n\n🤗 Good day to you 😎👌🔥 !!!\n\n")
                    break

    # TABLE AND LIST PRINT
    @staticmethod
    def table_show(table_name, columns, rows, options=None):
        """tool to print tables"""
        table = Table(title=table_name, style="bold", show_lines=True)

        for column in columns:
            column_options = options.get(column, {}) if options else {}
            table.add_column(column, **column_options)

        for row in rows:
            table.add_row(*row)

        console = Console()
        console.print(table, style="gold1")
        return

    @staticmethod
    def show_compact_list(title, items, item_label):
        """Display a compact list of items with IDs and labels."""
        # Get terminal width
        terminal_width = shutil.get_terminal_size().columns
        # Print the title and separator
        print(f"\n{View.GREEN}{title}:")
        current_line_length = 0
        items_list = []
        for item in items:
            item_output = f"{View.YELLOW}{item.id}: {View.MAGENTA}{getattr(item, item_label)} {View.BLUE}| "

            # Check if adding the next item exceeds the terminal width
            if current_line_length + len(item_output) > terminal_width:
                # Move to the next line
                print()
                current_line_length = 0

            # Print the item and update the current line length
            print(item_output, end="")
            current_line_length += len(item_output)

            # Keep track of the IDs
            items_list.append(item.id)
        return items_list

    # MENU LAYOUT
    @staticmethod
    def menu(header, menu_options):
        """Displays a type menu with information in parameters"""
        View.clear_screen()
        spc = " "
        epic1 = " █▀▀ █▀█ █ ▄▀▀"
        epic2 = "█▀  █▀▀ █ █"
        epic3 = " ▀▀▀ ▀   ▀  ▀▀"

        events1 = " _____   _____ _  _ _____ ___ "
        events2 = r"| __\ \ / / __| \| |_   _/ __|"
        events3 = r"| _| \ V /| _|| .` | | | \__ \ "
        events4 = r"|___| \_/ |___|_|\_| |_| |___/"

        View.prt_green(f"{spc*9}#################################################")
        View.prt_red(f"{spc*9}░▒░▒░▒░▒ 🎉 {epic1.center(26)} 🎈 ▒░▒░▒░▒")
        View.prt_green(f"{spc*9}░▒▀▄░▒░▒   🥂{epic2.center(24)}🍾   ▒░▒▄▀░▒")
        View.prt_red(f"{spc*9}░▒░▒░▒░▒  {epic3.center(30)}  ▒░▒░▒░▒")
        View.prt_yellow(f"{spc*9}░▒░       {spc.center(30)}      ▒░▒")
        View.prt_yellow(f"{spc*9}░▒░ {header.center(41)} ▒░▒")
        View.prt_yellow(f"{spc*9}░▒░       {events1.center(30)}      ▒░▒")
        View.prt_red(f"{spc*9}░▒░▒░▒░▒  {events2.center(30)}  ▒░▒░▒░▒")
        View.prt_green(f"{spc*9}░▒▄▀░▒░▒  {events3.center(30)} ▒░▒▀▄░▒")
        View.prt_red(f"{spc*9}░▒░▒░▒░▒  {events4.center(30)}  ▒░▒░▒░▒")
        View.prt_green(f"{spc*9}#################################################\n")
        if menu_options != []:
            View.prt_blue("Menu :")
            options = "\n".join(f"{spc*18}{option}" for option in menu_options)
            View.prt_yellow(options)
            View.prt_blue_no_carriage_return("\nEnter your choice : ")
        else:
            # if menu_options is an empty list, display the asciiart above without options
            return

    @staticmethod
    def clear_screen():
        """clears the screen before displaying menu or information pages"""
        os.system("cls" if os.name == "nt" else "clear")
