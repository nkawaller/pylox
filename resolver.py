"""Class that performs a variable resolution pass"""

import expr
import stmt


class Resolver(expr.Visitor, stmt.Visitor):
    """Implements expr and stmt visitors because we visit every node
    in the syntax tree
    """
    
    scopes = []

    def __init__(self, interpreter):
        self.interpreter = interpreter

    def visit_block_stmt(self, s):
        self.begin_scope()
        self.resolve(s.statements)
        self.endScope()
        return None

    def visit_var_stmt(self, s):
        self.declare(s.name)
        # TODO: shorten this
        if s.initializer is not None:
            self.resolve(s.initializer)
        self.define(s.name)
        return None

    def resolve(self, statements):
        for statement in statements:
            self.resolve_stmt(statement)

    def resolve_stmt(self, s):
        s.accept(self)

    def resolve_expr(self, e):
        e.accept(self)

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name):
        if not self.scopes: return
        # Using last index instead of peek()
        scope = self.scopes[-1]
        scope[name.lexeme] = False

    def define(self, name):
        if not self.scopes: return
        # Using last index instead of peek()
        self.scopes[-1][name.lexeme] = True
    