"""Function class"""

import environment
import loxcallable
import returnvalue


class LoxFunction(loxcallable.LoxCallable):

    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure

    def to_string(self):
        return f"<fn {self.declaration.name.lexeme}>"

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        env = environment.Environment(self.closure)
        for i in range(len(self.declaration.params)):
            env.define(
                self.declaration.params[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, env)
        except returnvalue.Return as r:
            return r.value
        return None