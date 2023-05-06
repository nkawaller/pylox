"""Function class"""

import environment
import loxcallable


class LoxFunction(loxcallable.LoxCallable):

    def __init__(self, declaration):
        self.declaration = declaration

    def call(self, interpreter, arguments):
        env = environment.Environment(interpreter.globals)
        for i in len(self.declaration.params):
            #TODO: this syntax isn't right
            env.define(self.declaration.params.get(i).lexeme, arguments.get(i))
        interpreter.execute_block(self.declaration.body, env)
        return None