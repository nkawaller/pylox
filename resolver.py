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
        NONE = ""
        FUNCTION = ""
    
    scopes = []
    current_fn = FunctionType.NONE

    def __init__(self, interpreter):
        self.interpreter = interpreter

    def visit_block_stmt(self, s):
        self.begin_scope()
        self.resolve(s.statements)
        self.endScope()
        return None

    def visit_expression_stmt(self, s):
        # TODO: should this call resolve_expr or just resolve?
        # Or should I just have resolve() handle both?
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
        if s.value: 
            self.resolve(s.value)
        return None

    def visit_var_stmt(self, s):
        self.declare(s.name)
        # TODO: shorten this
        if s.initializer is not None:
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
        self.resolveLocal(e, e.name)
        return None

    def visit_binary_expr(self, e):
        self.resolve(e.right)
        self.resolve(e.left)

    def visit_call_expr(self, e):
        self.resolve(e.callee)
        for argument in e.arguments:
            self.resolve(argument)
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

    def visit_unary_expr(self, e):
        self.resolve(e.right)
        return None

    def visit_variable_expr(self, e):
        # TODO: do I need Boolean.False here?
        if self.scopes and self.scopes[-1][e.name.lexeme] == False:
            lox.Lox.error(e.name, 
                "Can't read local variable in its own initializer.")
        self.resolve_local(e, e.name)
        return None

    # def resolve(self, X):
    #     for i in X:
    #         i.accept(self)
            
    def resolve(self, statements):
        for statement in statements:
            self.resolve_stmt(statement)

    def resolve_stmt(self, s):
        s.accept(self)

    def resolve_expr(self, e):
        e.accept(self)

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
    