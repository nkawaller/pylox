"""Interpreter class"""

import expr

class Interpreter(expr.Visitor):
    """Using the visitor pattern, execute the syntax tree itself"""
    
    def visit_literal_expr(e):
        """Evaluate literal expressions"""

        return e.value

    def visit_grouping_expr(self, e):
        """Evaluate grouping expressions"""

        return self.evaluate(e.expression)

    def evaluate(self, e):
        return e.accept(self)