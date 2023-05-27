"""Function class"""

import environment
import loxcallable
import returnvalue


class LoxFunction(loxcallable.LoxCallable):
    def __init__(self, declaration, closure, is_initializer):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def bind(self, instance):
        env = environment.Environment(self.closure)
        env.define("this", instance)
        return LoxFunction(self.declaration, env, self.is_initializer)

    def to_string(self):
        return f"<fn {self.declaration.name.lexeme}>"

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        env = environment.Environment(self.closure)
        for i in range(len(self.declaration.params)):
            env.define(self.declaration.params[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, env)
        except returnvalue.Return as r:
            if self.is_initializer:
                return self.closure.get_at(0, "this")
            return r.value
        if self.is_initializer:
            return self.closure.get_at(0, "this")
        return None
