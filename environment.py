"""Class to store bindings that map values to variable names"""

from runtimeexception import RuntimeException


class Environment:
    """Environment class"""

    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def get(self, name):
        """Look up a variable name

        :param name: Token
        :return: Token.lexeme
        """
        if name.lexeme in self.values:
            return self.values.get(name.lexeme, None)
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise RuntimeException(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        raise RuntimeException(name, f"Undefined variable '{name.lexeme}'.")

    def define(self, name, value):
        """Define variables by binding a name to a value. Reassigning
        variables is allowed.
        """
        self.values[name] = value

    def ancestor(self, distance):
        environment = self
        for _ in range(distance):
            environment = environment.enclosing
        return environment

    def get_at(self, distance, name):
        return self.ancestor(distance).values.get(name)

    def assign_at(self, distance, name, value):
        self.ancestor(distance).values[name.lexeme] = value
