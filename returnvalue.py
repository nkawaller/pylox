"""Lox Return Class"""


class Return(Exception):
    """Lox class that inherits from python's exception class so we
    unwind the call stack when return statements are executed
    """

    def __init__(self, value):
        super().__init__()
        self.value = value