"""Class to store bindings that map values to variable names"""

import runtimeexception


class Environment:
    """Environment class"""

    def __init__(self):
        self.values = {}

    def get(self, name):
        """Look up a variable name
        
        :param name: Token
        :return: Token.lexeme
        """
        if name.lexeme in self.values:
            return self.values.get(name.lexeme, None)
        raise runtimeexception.RuntimeException(
            name, f"Undefined variable '{name.lexeme}'.")

    def define(self, name, value):
        """Define variables by binding a name to a value. Reassigning
        variables is allowed.
        """
        self.values[name] = value
