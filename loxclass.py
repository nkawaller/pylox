"""Class to represent Lox classes"""

import loxcallable as lc
import loxinstance as li


class LoxClass(lc.LoxCallable):
    """Uses call expressions on class objects to create new
    instances - kind of like a factory function that generates
    instances of itself.
    """

    def __init__(self, name, superclass, methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods          # TODO: this was supposed to be a cls property; may need to revisit

    def __str__(self):
        return self.name

    def find_method(self, name):
        if name in self.methods:
            return self.methods[name]
        if self.superclass:
            return self.superclass.find_method(name)
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
