"""Interpreter class"""

import environment
import expr
import runtimeexception
import stmt
import tokentypes


class Interpreter(expr.Visitor, stmt.Visitor):
    """Using the visitor pattern, execute the syntax tree itself"""

    environment = environment.Environment()

    def interpret(self, statements):
        try:
            for s in statements:
                self.execute(s)
        except RuntimeError as e:
            runtimeexception.RuntimeException(e)

    def visit_print_stmt(self, s):
        value = self.evaluate(s.expression)
        print(self.stringify(value))
        return None

    def visit_var_stmt(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None

    def visit_assign_expr(self, e):
        value = self.evaluate(e.value)
        self.environment.assign(e.name, value)
        return value
        
    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expression)
        return None

    def visit_literal_expr(self, e):
        """Evaluate literal expressions"""

        return e.value

    def visit_grouping_expr(self, e):
        """Evaluate grouping expressions"""

        return self.evaluate(e.expression)

    def visit_unary_expr(self, e):
        """Evaluate unary expressions"""

        right = self.evaluate(e.right)

        unary_map = {
            tokentypes.TokenType.BANG: lambda right: not self.is_truthy(right),
            tokentypes.TokenType.MINUS: lambda right, op=e.operator: (
                -float(right) if self.check_number_operand(op, right) else None
            ),
        }

        return unary_map.get(e.operator.tokentype, None)(right)

    def visit_variable_expr(self, e):
        return self.environment.get(e.name)

    def check_number_operand(self, operator, operand):
        if isinstance(operand, float):
            return True
        raise runtimeexception.RuntimeException(operator, "Operand must be a number")

    def check_number_operands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return True
        raise runtimeexception.RuntimeException(operator, "Operands must be a numbers")

    def is_truthy(self, object):
        """Evaluate an object's truthiness. False and Nil are false,
        everything else is true
        """

        if object is None:
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

    def stringify(self, object):
        """Convert object to a string and display to user"""

        if object is None:
            return "nil"
        if isinstance(object, float):
            text = str(object)
            if text.endswith(".0"):
                text = text[0 : len(text) - 2]
            return text
        return str(object)

    def evaluate(self, e):
        """Send the expression back into the interpreter's visitor
        implementation
        """

        return e.accept(self)

    def execute(self, statement):
        statement.accept(self)

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for s in statements:
                self.execute(s)
        finally:
            self.environment = previous

    def visit_block_stmt(self, s):
        self.execute_block(s.statements, environment.Environment(self.environment))
        return None

    def handle_arithmetic_operator(self, left, right, op):
        """Determine which type the + operator is acting on"""

        if isinstance(left, float) and isinstance(right, float):
            return float(left) + float(right)
        if isinstance(left, str) and isinstance(right, str):
            return str(left) + str(right)
        raise runtimeexception.RuntimeException(
            op, "Operators must be two numbers or two strings"
        )

    def visit_binary_expr(self, e):
        """Evaluate binary expressions"""

        left = self.evaluate(e.left)
        right = self.evaluate(e.right)

        binary_map = {
            tokentypes.TokenType.MINUS: lambda left, right, op=e.operator: (
                float(left) - float(right)
                if self.check_number_operands(op, left, right)
                else None
            ),
            tokentypes.TokenType.SLASH: lambda left, right, op=e.operator: (
                float(left) / float(right)
                if self.check_number_operands(op, left, right)
                else None
            ),
            tokentypes.TokenType.STAR: lambda left, right, op=e.operator: (
                float(left) * float(right)
                if self.check_number_operands(op, left, right)
                else None
            ),
            tokentypes.TokenType.PLUS: lambda left, right, op=e.operator: self.handle_arithmetic_operator(
                left, right, op
            ),
            tokentypes.TokenType.GREATER: lambda left, right, op=e.operator: (
                float(left) > float(right)
                if self.check_number_operands(op, left, right)
                else None
            ),
            tokentypes.TokenType.GREATER_EQUAL: lambda left, right, op=e.operator: (
                float(left) >= float(right)
                if self.check_number_operands(op, left, right)
                else None
            ),
            tokentypes.TokenType.LESS: lambda left, right, op=e.operator: (
                float(left) < float(right)
                if self.check_number_operands(op, left, right)
                else None
            ),
            tokentypes.TokenType.LESS_EQUAL: lambda left, right, op=e.operator: (
                float(left) <= float(right)
                if self.check_number_operands(op, left, right)
                else None
            ),
            tokentypes.TokenType.BANG_EQUAL: lambda left, right: not self.is_equal(
                left, right
            ),
            tokentypes.TokenType.EQUAL_EQUAL: lambda left, right: self.is_equal(
                left, right
            ),
        }

        return binary_map.get(e.operator.tokentype, None)(left, right)
