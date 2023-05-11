"""Class that performs a variable resolution pass"""

import expr
import stmt


class Resolver(expr.Visitor, stmt.Visitor):
    """Implements expr and stmt visitors because we visit every node
    in the syntax tree
    """

    def __init__(self, interpreter):
        self.interpreter = interpreter

    def visit_block_stmt(self, s):
        self.begin_scope()
        self.resolve(s.statements)
        self.endScope()
        return None

    def resolve(self, statements):
        for statement in statements:
            self.resolve_stmt(statement)

    def resolve_stmt(self, s):
        s.accept(self)

    def resolve_expr(self, e):
        e.accept(self)
