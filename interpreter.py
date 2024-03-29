"""Interpreter class"""

import clock
import expr
import stmt
from environment import Environment
from loxcallable import LoxCallable
from loxclass import LoxClass
from loxfunction import LoxFunction
from loxinstance import LoxInstance
from returnvalue import Return
from runtimeexception import RuntimeException
from tokentypes import TokenType


class Interpreter(expr.Visitor, stmt.Visitor):
    """Using the visitor pattern, execute the syntax tree itself"""

    def __init__(self):
        self.globals = Environment()     # fixed reference to outermost global scope
        self.environment = self.globals              # keeps track of current environment
        self.globals.define("clock", clock.Clock())  # add 'clock' key:val to the global environment
        self.locals = {}

    def interpret(self, statements):
        try:
            for s in statements:
                self.execute(s)
        except RuntimeError as e:
            RuntimeException(e)

    def visit_print_stmt(self, s):
        value = self.evaluate(s.expression)
        print(self.stringify(value))
        return None

    def visit_return_stmt(self, s):
        value = None
        if s.value is not None:
            value = self.evaluate(s.value)
        raise Return(value)

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
        distance = self.locals.get(e, None)
        if distance:
            self.environment.assign_at(distance, e.name, value)
        else:
            self.globals.assign(e.name, value)
        return value

    def visit_expression_stmt(self, s):
        self.evaluate(s.expression)
        return None

    def visit_function_stmt(self, s):
        """Take a compile-time representation of the function and 
        convert it to its runtime representation
        """

        function = LoxFunction(s, self.environment, False)
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
        if e.operator.tokentype == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left
        return self.evaluate(e.right)

    def visit_set_expr(self, e):
        object = self.evaluate(e.object)
        if not isinstance(object, LoxInstance):
            raise RuntimeException(
                e.name, "Only instances have fields."
            )
        value = self.evaluate(e.value)
        object.set(e.name, value)
        return value

    def visit_super_expr(self, e):
        distance = self.locals.get(e)
        superclass = self.environment.get_at(distance, "super")
        object = self.environment.get_at(distance - 1, "this")
        method = superclass.find_method(e.method.lexeme)
        if method is None:
            raise RuntimeException(e.method,
                f"Undefined property '{e.method.lexeme}'.")
        return method.bind(object)

    def visit_this_expr(self, e):
        return self.lookup_variable(e.keyword, e)

    def visit_grouping_expr(self, e):
        """Evaluate grouping expressions"""

        return self.evaluate(e.expression)

    def visit_unary_expr(self, e):
        """Evaluate unary expressions"""

        right = self.evaluate(e.right)

        unary_map = {
            TokenType.BANG: lambda right: not self.is_truthy(right),
            TokenType.MINUS: lambda right, op=e.operator: (
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
        raise RuntimeException(operator, "Operand must be a number")

    def check_number_operands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return True
        raise RuntimeException(operator, "Operands must be a numbers")

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
        self.execute_block(s.statements, Environment(self.environment))
        return None

    def visit_class_stmt(self, s):
        superclass = None
        if s.superclass:
            superclass = self.evaluate(s.superclass)
            if not isinstance(superclass, LoxClass):
                raise RuntimeException(
                    s.superclass.name, "Superclass must be a class.")
        self.environment.define(s.name.lexeme, None)
        if s.superclass:
            self.environment = Environment(self.environment)
            self.environment.define("super", superclass)
        methods = {}
        for method in s.methods:
            fn = LoxFunction(
                method, self.environment, method.name.lexeme == "init")
            methods[method.name.lexeme] = fn
        klass = LoxClass(s.name.lexeme, superclass, methods)
        if superclass:
            self.environment = self.environment.enclosing
        self.environment.assign(s.name, klass)
        return None

    def handle_arithmetic_operator(self, left, right, op):
        """Determine which type the + operator is acting on"""

        if isinstance(left, float) and isinstance(right, float):
            return float(left) + float(right)
        if isinstance(left, str) and isinstance(right, str):
            return str(left) + str(right)
        raise RuntimeException(
            op, "Operators must be two numbers or two strings"
        )

    def visit_binary_expr(self, e):
        """Evaluate binary expressions"""

        left = self.evaluate(e.left)
        right = self.evaluate(e.right)

        binary_map = {
            TokenType.MINUS: lambda left, right, op=e.operator: (
                float(left) - float(right)
                if self.check_number_operands(op, left, right)
                else None
            ),
            TokenType.SLASH: lambda left, right, op=e.operator: (
                float(left) / float(right)
                if self.check_number_operands(op, left, right)
                else None
            ),
            TokenType.STAR: lambda left, right, op=e.operator: (
                float(left) * float(right)
                if self.check_number_operands(op, left, right)
                else None
            ),
            TokenType.PLUS: lambda left, right, op=e.operator: self.handle_arithmetic_operator(
                left, right, op
            ),
            TokenType.GREATER: lambda left, right, op=e.operator: (
                float(left) > float(right)
                if self.check_number_operands(op, left, right)
                else None
            ),
            TokenType.GREATER_EQUAL: lambda left, right, op=e.operator: (
                float(left) >= float(right)
                if self.check_number_operands(op, left, right)
                else None
            ),
            TokenType.LESS: lambda left, right, op=e.operator: (
                float(left) < float(right)
                if self.check_number_operands(op, left, right)
                else None
            ),
            TokenType.LESS_EQUAL: lambda left, right, op=e.operator: (
                float(left) <= float(right)
                if self.check_number_operands(op, left, right)
                else None
            ),
            TokenType.BANG_EQUAL: lambda left, right: not self.is_equal(
                left, right
            ),
            TokenType.EQUAL_EQUAL: lambda left, right: self.is_equal(
                left, right
            ),
        }

        return binary_map.get(e.operator.tokentype, None)(left, right)

    def visit_call_expr(self, e):
        callee = self.evaluate(e.callee)
        arguments = []
        for argument in e.arguments:
            arguments.append(self.evaluate(argument))
        if not isinstance(callee, LoxCallable):
            raise RuntimeException(
                e.paren, "Can only call functions and classes.")
        function = callee
        if len(arguments) != function.arity():
            raise RuntimeException(
                e.paren, f"Expected {function.arity()} arguments but got {len(arguments)}.")
        return function.call(self, arguments)

    def visit_get_expr(self, e):
        object = self.evaluate(e.object)
        if isinstance(object, LoxInstance):
            return object.get(e.name)
        raise RuntimeException(
            "Only instances have properties."
        )
