from .view import View


class ErrorView(View):

    @staticmethod
    def alert(text):
        View.prt_red(text)
