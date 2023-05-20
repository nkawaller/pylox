"""Interpreter class"""

import clock
import environment
import expr
import loxfunction
import loxcallable
import returnvalue
import runtimeexception
import stmt
import tokentypes


class Interpreter(expr.Visitor, stmt.Visitor):
    """Using the visitor pattern, execute the syntax tree itself"""

    def __init__(self):
        self.globals = environment.Environment()     # fixed reference to outermost global scope
        self.environment = self.globals              # keeps track of current environment
        self.globals.define("clock", clock.Clock())  # add 'clock' key:val to the global environment
        self.locals = {}

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

    def visit_return_stmt(self, s):
        value = None
        if s.value is not None:
            value = self.evaluate(s.value)
        raise returnvalue.Return(value)

    def visit_var_stmt(self, s):
        value = None
        if s.initializer is not None:
            value = self.evaluate(s.initializer)
        self.environment.define(s.name.lexeme, value)
        return None

    def visit_while_stmt(self, s):
        """Execute the while statment body until the condition is no
        longer true
        """
        while self.is_truthy(self.evaluate(s.condition)):
            self.execute(s.body)
        return None

    def visit_assign_expr(self, e):
        value = self.evaluate(e.value)
        # Should this be: distance = self.locals.get(e.name)
        distance = self.locals.get(e, None)
        if distance:
            self.environment.assign_at(distance, e.name, value)
        else:
            self.globals.assign(e.name, value)
        return value
        
    def visit_expression_stmt(self, stmt):
        # TODO: rename to s?
        self.evaluate(stmt.expression)
        return None

    def visit_function_stmt(self, s):
        """Take a compile-time representation of the function and 
        convert it to its runtime representation
        """

        function = loxfunction.LoxFunction(s, self.environment)
        # Bind fn to a var in current environment
        self.environment.define(s.name.lexeme, function)
        return None

    def visit_if_stmt(self, s):
        """Execute if branch if it evaluates to True. Otherwise 
        execute the else branch (if there is one)
        """

        if self.is_truthy(self.evaluate(s.condition)):
            self.execute(s.then_branch)
        elif s.else_branch is not None:
            self.execute(s.else_branch)
        return None

    def visit_literal_expr(self, e):
        """Evaluate literal expressions"""

        return e.value

    def visit_logical_expr(self, e):
        """Evaluate logical expressions"""

        left = self.evaluate(e.left)
        if e.operator.tokentype == tokentypes.TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                    return left
        return self.evaluate(e.right)

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
        return self.lookup_variable(e.name, e)

    def lookup_variable(self, name, e):
        distance = self.locals.get(e, None)         # Python dict built-in get()
        if distance is not None:                    # Looking for an int, not a boolean
            return self.environment.get_at(distance, name.lexeme)
        else:
            return self.globals.get(name)           # Environment method get(), not python's

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

    def resolve(self, e, depth):
        self.locals[e] = depth

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

    def visit_call_expr(self, e):
        callee = self.evaluate(e.callee)
        arguments = []
        for argument in e.arguments:
            arguments.append(self.evaluate(argument))
        if not isinstance(callee, loxcallable.LoxCallable):
            raise runtimeexception.RuntimeException(
                e.paren, "Can only call functions and classes.")
        function = callee
        if len(arguments) != function.arity():
            raise runtimeexception.RuntimeException(
                e.paren, f"Expected {function.arity()} arguments but got {len(arguments)}.")
        return function.call(self, arguments)
