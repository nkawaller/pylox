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

    def visit_unary_expr(self, e):
        """Evaluate unary expressions"""

        right = self.evaluate(e.right)

        # if e.operator.tokentype == "BANG":
        #     return not self.is_truthy(right)
        # if e.operator.tokentype == "MINUS":
        #     return -float(right)

        unary_map = {
            "BANG": lambda right: not self.is_truthy(right),
            "MINUS": lambda right: -float(right)
        }

        return unary_map.get(e.operator.tokentype, None)(right)

    def is_truthy(self, object):
        """Evaluate an object's truthiness. False and Nil are false,
        everything else is true
        """

        if object == None:
            return False
        if isinstance(object, bool):
            return bool(object)
        return True

    def evaluate(self, e):
        """Send the expression back into the interpreter's visitor
        implementation
        """

        return e.accept(self)
