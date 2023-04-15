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

        unary_map = {
            "BANG": lambda right: not self.is_truthy(right),
            # checkOperand Here
            "MINUS": lambda right: -float(right)
        }

        return unary_map.get(e.operator.tokentype, None)(right)

    def check_number_operand(operator, operand):
        if isinstance(operand, float): return
        raise RuntimeException(operator, "Operand must be a number")
        
    def is_truthy(self, object):
        """Evaluate an object's truthiness. False and Nil are false,
        everything else is true
        """

        if object == None:
            return False
        if isinstance(object, bool):
            return bool(object)
        return True

    def is_equal(self, a, b):
        """Determine equality"""

        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def evaluate(self, e):
        """Send the expression back into the interpreter's visitor
        implementation
        """

        return e.accept(self)

    def handle_arithmetic_operator(self, left, right):
        """Determine which type the + operator is acting on"""

        if isinstance(left, float) and isinstance(right, float):
            return float(left) + float(right)
        if isinstance(left, str) and isinstance(right, str):
            return str(left) + str(right)

    def visit_binary_expr(self, e):
        """Evaluate binary expressions"""

        left = self.evaluate(e.left)
        right = self.evaluate(e.right)

        binary_map = {
            "MINUS": lambda left, right: float(left) - float(right),
            "SLASH": lambda left, right: float(left) / float(right),
            "STAR": lambda left, right: float(left) * float(right),
            "PLUS": lambda left, right: self.handle_arithmetic_operator(left, right),
            "GREATER": lambda left, right: float(left) > float(right),
            "GREATER_EQUAL": lambda left, right: float(left) >= float(right),
            "LESS": lambda left, right: float(left) < float(right),
            "LESS_EQUAL": lambda left, right: float(left) <= float(right),
            "BANG_EQUAL": lambda left, right: not self.is_equal(left, right),
            "EQUAL_EQUAL": lambda left, right: self.is_equal(left, right)
        }

        return binary_map.get(e.operator.tokentype, None)(left, right)
