"""Lox runtime error class"""

class RuntimeException(RuntimeError):

    def __init__(self, token, message):
        #TODO: add super(message)
        self.token = token