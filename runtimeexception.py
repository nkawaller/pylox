"""Lox runtime error class"""


class RuntimeException(Exception):
    """Custom Lox exception that inherits from python's exception"""

    def __init__(self, token, message) -> None:
        super().__init__(message)
        self.token = token
