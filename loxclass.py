"""Class to represent Lox classes"""

import loxcallable as lc
import loxinstance as li


class LoxClass(lc.LoxCallable):
    """Uses call expressions on class objects to create new 
    instances - kind of like a factory function that generates 
    instances of itself.
    """

    def __init__(self, name, methods):
        self.name = name
        self.methods = methods          # TODO: this was supposed to be a cls property; may need to revisit

    def __str__(self):
        return self.name

    def find_method(self, name):
        if name in self.methods:
            return self.methods[name]
        return None

    def call(self, interpreter, arguments):
        instance = li.LoxInstance(self)
        initializer = self.find_method("init")
        if initializer:
            initializer.bind(instance).call(interpreter, arguments)
        return instance

    def arity(self):
        initializer = self.find_method("init")
        if not initializer:
            return 0
        return initializer.arity()