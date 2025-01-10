import re
from datetime import datetime

from views.error_view import ErrorView


class Input:
    @staticmethod
    def _input(prompt):
        """Replace input() displaying prompt in blue and releasing in yellow for answers."""
        BLUE = "\x1B[94m"
        RESET = "\x1B[93m"
        return input(f"{BLUE}{prompt}{RESET}")

    @staticmethod
    def integer(prompt, choices=None, upd=False):
        while True:
            try:
                user_input = Input._input(prompt)
                if user_input.strip() == "" and upd:
                    return
                else:
                    result = int(user_input)
            except ValueError:
                ErrorView().alert("the response has to be an integer")
                continue
            if choices and result not in choices:
                ErrorView().alert("this value is not part of the possible choices")
                continue
            return result

    @staticmethod
    def float(prompt, limit=None, choices=None, upd=False):
        while True:
            try:
                user_input = Input._input(prompt)
                if user_input.strip() == "" and upd:
                    return
                else:
                    result = float(user_input)
            except ValueError:
                ErrorView().alert("the response has to be an integer or a float")
                continue
            if choices and result not in choices:
                ErrorView().alert("this value is not part of the possible choices")
                continue
            if limit is not None:
                if result > limit:
                    ErrorView().alert("this value should be lower than Total Amount Value")
                    continue
            return result

    @staticmethod
    def string(prompt, choices=None, upd=False):
        while True:
            try:
                user_input = Input._input(prompt)
                if user_input.strip() == "" and upd:
                    return
                else:
                    result = str(user_input).strip()
            except ValueError:
                ErrorView().alert("the response has to be a string")
                continue
            if choices and result not in choices:
                ErrorView().alert("this response is not part of the possible choices")
                continue
            return result

    @staticmethod
    def string_name(prompt, choices=None, upd=False):
        while True:
            try:
                user_input = Input._input(prompt)
                if user_input.strip() == "" and upd:
                    return
                else:
                    result = str(user_input).strip()
            except ValueError:
                ErrorView().alert("the response has to be an string name")
                continue
            if choices and result not in choices:
                ErrorView().alert("this value is not part of the possible choices")
                continue
            if result == "" or re.match("^[-' a-zA-ZÀ-ÿ]+$", result) is None:
                ErrorView().alert("Please give a valid response (a string for... a name ?)")
                continue
            return result

    @staticmethod
    def date(prompt, upd=False):
        while True:
            user_input = Input._input(prompt)
            if user_input.strip() == "" and upd:
                return
            else:
                result = user_input.strip()
            if (
                result == ""
                or re.match(
                    r"^(3[01]|[12][0-9]|0?[1-9])(\/|\-|\.)"
                    r"(1[0-2]|0?[1-9])\2([12][0-9]{3}) "
                    r"((2[0-3]|[01][0-9])(:)[0-5]?[0-9]"
                    r"(:)[0-5]?[0-9])$",
                    result,
                )
                is None
            ):
                ErrorView().alert("Please give a valid date (29/12/2025 17:30:59)")
                continue
            return result

    @staticmethod
    def event_date(prompt, upd=False):
        while True:
            user_input = Input._input(prompt)
            if user_input.strip() == "" and upd:
                return
            else:
                result = user_input.strip()
            if (
                result == ""
                or re.match(
                    r"^(3[01]|[12][0-9]|0?[1-9]) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
                    r" ([12][0-9]{3}) @ (1[0-2]|0?[1-9])(AM|PM)$",
                    result,
                )
                is None
            ):
                ErrorView().alert("Please give a valid date (e.g.: 4 Jun 2023 @ 1PM )")
                continue
            return result

    @staticmethod
    def date_default_to_now(prompt, upd=False):
        while True:
            result = Input._input(prompt).strip()
            if result == "":
                result = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
            if (
                result == ""
                or re.match(
                    r"^(3[01]|[12][0-9]|0?[1-9])(\/|\-|\.)"
                    r"(1[0-2]|0?[1-9])\2([12][0-9]{3}) "
                    r"((2[0-3]|[01][0-9])(:)[0-5]?[0-9]"
                    r"(:)[0-5]?[0-9])$",
                    result,
                )
                is None
            ):
                ErrorView().alert("Please give a valid date (29/12/2025 17:30:59)")
                continue
            return result

    @staticmethod
    def email(prompt, choices=None, upd=False):
        while True:
            user_input = Input._input(prompt)
            if user_input.strip() == "" and upd:
                return
            else:
                result = str(user_input).strip()
            if result == "" or re.match(r"[^@]+@[^@]+\.[^@]+", result) is None:
                ErrorView().alert("Please enter a valid email address")
                continue
            if choices and result not in choices:
                ErrorView().alert("this response is not part of the possible choices")
                continue
            return result

    @staticmethod
    def anything(prompt, choices=None, upd=False):
        while True:
            user_input = Input._input(prompt)
            if user_input.strip() == "" and upd:
                return
            else:
                result = str(user_input).strip()
            if result == "":
                ErrorView().alert("Please give a valid input")
                continue
            if choices and result not in choices:
                ErrorView().alert("this response is not part of the possible choices")
                continue
            return result

    @staticmethod
    def phone_number(prompt, choices=None, upd=False):
        while True:
            user_input = Input._input(prompt)
            if user_input.strip() == "" and upd:
                return
            else:
                result = user_input.strip()
            if result == "" or re.match(r"^\+?[0-9]+(?: [0-9]+)*$", result) is None:
                ErrorView().alert("Please give a valid phone number (e.g. 06 68 15 24 64 or +33 6 78 989 515)")
                continue
            return result

    @staticmethod
    def company_name(prompt, choices=None, upd=False):
        while True:
            user_input = Input._input(prompt)
            if user_input.strip() == "" and upd:
                return
            else:
                result = user_input.strip()
            if result == "" or re.match(r"^[a-zA-Z0-9À-ÖØ-öø-ÿ&'’\"()\-.,\s]+$", result) is None:
                ErrorView().alert("Please give a valid company name")
                continue
            return result

    @staticmethod
    def role(prompt, choices=None, upd=False):
        while True:
            user_input = Input._input(prompt)
            if user_input.strip() == "" and upd:
                return
            else:
                result = user_input.strip().upper()
            if result == "" or result.strip().upper() not in ["MANAGEMENT", "COMMERCIAL", "SUPPORT"]:
                ErrorView().alert("Please enter a valid role : MANAGEMENT or COMMERCIAL or SUPPORT")
                continue
            return result

    @staticmethod
    def signed_contract(prompt, choices=None, upd=False):
        while True:
            user_input = Input._input(prompt)
            if user_input.strip() == "" and upd:
                return
            else:
                result = user_input.strip()
            if result == "" or result.lower() not in ["unsigned", "signed"]:
                ErrorView().alert("Please enter a valid status : signed or unsigned")
                continue
            return result
