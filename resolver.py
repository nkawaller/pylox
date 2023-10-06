"""Class that performs a variable resolution pass"""


import lox
import expr
import stmt
from enum import Enum


class Resolver(expr.Visitor, stmt.Visitor):
    """Implements expr and stmt visitors because we visit every node
    in the syntax tree
    """

    class FunctionType(Enum):
        NONE = "NONE"
        FUNCTION = "FUNCTION"
        METHOD = "METHOD"
        INITIALIZER = "INITIALIZER"

    class ClassType(Enum):
        NONE = "NONE"
        CLASS = "CLASS"
        SUBCLASS = "SUBCLASS"

    scopes = []
    current_fn = FunctionType.NONE
    current_cls = ClassType.NONE

    def __init__(self, interpreter):
        self.interpreter = interpreter

    def visit_block_stmt(self, s):
        self.begin_scope()
        self.resolve(s.statements)
        self.end_scope()
        return None

    def visit_class_stmt(self, s):
        enclosing_cls = self.current_cls
        self.current_cls = self.ClassType.CLASS
        self.declare(s.name)
        self.define(s.name)
        if s.superclass and s.name.lexeme == s.superclass.name.lexeme:
            lox.Lox.error(s.superclass.name,
                "A class can't inherit from itself.")
        if s.superclass:
            self.current_cls = self.ClassType.SUBCLASS
            self.resolve(s.superclass)
        if s.superclass:
            self.begin_scope()
            self.scopes[-1]["super"] = True
        self.begin_scope()
        # using last index instead of peek()
        self.scopes[-1]["this"] = True
        for method in s.methods:
            declaration = self.FunctionType.METHOD
            if method.name.lexeme == "init":
                declaration = self.FunctionType.INITIALIZER
            self.resolve_function(method, declaration)
        self.end_scope()
        if s.superclass:
            self.end_scope()
        self.current_cls = enclosing_cls
        return None

    def visit_expression_stmt(self, s):
        self.resolve(s.expression)
        return None

    def visit_function_stmt(self, s):
        self.declare(s.name)
        self.define(s.name)
        self.resolve_function(s, self.FunctionType.FUNCTION)
        return None

    def visit_if_stmt(self, s):
        """Unlike interpretation, there is no control flow in 
        resolving. We visit both branches
        """

        self.resolve(s.condition)
        self.resolve(s.then_branch)
        if s.else_branch:
            self.resolve(s.else_branch)
        return None

    def visit_print_stmt(self, s):
        self.resolve(s.expression)
        return None

    def visit_return_stmt(self, s):
        if self.current_fn == self.FunctionType.NONE:
            lox.Lox.error(s.keyword, 
                "Can't return from top level code.")
        if s.value is not None:
            if self.current_fn == self.FunctionType.INITIALIZER:
                lox.Lox.error(s.keyword,
                    "Can't return a value from an initializer")
            self.resolve(s.value)
        return None

    def visit_var_stmt(self, s):
        self.declare(s.name)
        if s.initializer:
            self.resolve(s.initializer)
        self.define(s.name)
        return None

    def visit_while_stmt(self, s):
        """Resolve condition and body only once"""
        self.resolve(s.condition)
        self.resolve(s.body)
        return None

    def visit_assign_expr(self, e):
        self.resolve(e.value)
        self.resolve_local(e, e.name)
        return None

    def visit_binary_expr(self, e):
        self.resolve(e.right)
        self.resolve(e.left)
        return None

    def visit_call_expr(self, e):
        self.resolve(e.callee)
        for argument in e.arguments:
            self.resolve(argument)
        return None

    def visit_get_expr(self, e):
        self.resolve(e.object)
        return None

    def visit_grouping_expr(self, e):
        self.resolve(e.expression)
        return None

    def visit_literal_expr(self, e):
        return None

    def visit_logical_expr(self, e):
        self.resolve(e.left)
        self.resolve(e.right)
        return None

    def visit_set_expr(self, e):
        self.resolve(e.value)
        self.resolve(e.object)
        return None

    def visit_super_expr(self, e):
        if self.current_cls == self.ClassType.NONE:
            lox.Lox.error(e.keyword,
                "Can't use 'super' outside of a class.")
        elif self.current_cls != self.ClassType.SUBCLASS:
            lox.Lox.error(e.keyword,
                "can't use 'super' in a class with no superclass.")
        self.resolve_local(e, e.keyword)
        return None

    def visit_this_expr(self, e):
        if self.current_cls == self.ClassType.NONE:
            lox.Lox.error(e.keyword,
                "Can't use 'this' outisde of a class.")
            return None
        self.resolve_local(e, e.keyword)
        return None

    def visit_unary_expr(self, e):
        self.resolve(e.right)
        return None

    def visit_variable_expr(self, e):
        if self.scopes and self.scopes[-1].get(e.name.lexeme, None) == False:
            lox.Lox.error(e.name, 
                "Can't read local variable in its own initializer.")
        self.resolve_local(e, e.name)
        return None

    def resolve(self, input):
        if isinstance(input, list):
            for statement in input:
                statement.accept(self)
        else:
            input.accept(self)
            
    def resolve_function(self, fn, fn_type):
        enclosing_fn = self.current_fn
        self.current_fn = fn_type
        self.begin_scope()
        for param in fn.params:
            self.declare(param)
            self.define(param)
        self.resolve(fn.body)
        self.end_scope()
        self.current_fn = enclosing_fn

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name):
        if not self.scopes: return
        # Using last index instead of peek()
        scope = self.scopes[-1]
        if name.lexeme in scope:
            lox.Lox.error(name,
                "Already a variable with this name in this scope.")
        scope[name.lexeme] = False

    def define(self, name):
        if not self.scopes: return
        # Using last index instead of peek()
        self.scopes[-1][name.lexeme] = True

    def resolve_local(self, e, name):
        for i in range(len(self.scopes)-1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(e, len(self.scopes) - 1 - i)
                return
    
