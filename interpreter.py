"""Interpreter class"""

from typing_extensions import runtime
import expr
import runtimeexception

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
            "MINUS": lambda right: (-float(right) if self.check_number_operand() else None)
        }

        return unary_map.get(e.operator.tokentype, None)(right)

    def check_number_operand(operator, operand):
        if isinstance(operand, float): return True
        raise runtimeexception.RuntimeException(operator, "Operand must be a number")

    def check_number_operands(operator, left, right):
        if isinstance(left, float) and isinstance(right, float): return True
        raise runtimeexception.RuntimeException(operator, "Operands must be a numbers")
        
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

    def handle_arithmetic_operator(self, left, right, op):
        """Determine which type the + operator is acting on"""

        if isinstance(left, float) and isinstance(right, float):
            return float(left) + float(right)
        if isinstance(left, str) and isinstance(right, str):
            return str(left) + str(right)
        raise runtimeexception.RuntimeException(op, "Operators must be two numbers or two strings")

    def visit_binary_expr(self, e):
        """Evaluate binary expressions"""

        left = self.evaluate(e.left)
        right = self.evaluate(e.right)

        binary_map = {
            "MINUS": lambda left, right, op=e.operator: (float(left) - float(right) if self.check_number_operands(op, left, right) else None),
            "SLASH": lambda left, right, op=e.operator: (float(left) / float(right) if self.check_number_operands(op, left, right) else None),
            "STAR": lambda left, right, op=e.operator: (float(left) * float(right) if self.check_number_operands(op, left, right) else None),
            "PLUS": lambda left, right, op=e.operator: self.handle_arithmetic_operator(left, right, op),
            "GREATER": lambda left, right, op=e.operator: (float(left) > float(right) if self.check_number_operands(op, left, right) else None),
            "GREATER_EQUAL": lambda left, right, op=e.operator: (float(left) >= float(right) if self.check_number_operands(op, left, right) else None),
            "LESS": lambda left, right, op=e.operator: (float(left) < float(right) if self.check_number_operands(op, left, right) else None),
            "LESS_EQUAL": lambda left, right, op=e.operator: (float(left) <= float(right) if self.check_number_operands(op, left, right) else None),
            "BANG_EQUAL": lambda left, right: not self.is_equal(left, right),
            "EQUAL_EQUAL": lambda left, right: self.is_equal(left, right)
        }

        return binary_map.get(e.operator.tokentype, None)(left, right, e.operator)
