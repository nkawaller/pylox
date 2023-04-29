"""Syntax tree that represents the Lox grammar"""

from abc import ABC, abstractmethod

class Stmt(ABC):

	@abstractmethod
	def accept(self, visitor):
		pass

class Visitor(ABC):

	@abstractmethod
	def visit_block_stmt(self, stmt):
		pass

	@abstractmethod
	def visit_expression_stmt(self, stmt):
		pass

	@abstractmethod
	def visit_if_stmt(self, stmt):
		pass

	@abstractmethod
	def visit_print_stmt(self, stmt):
		pass

	@abstractmethod
	def visit_var_stmt(self, stmt):
		pass

class Block(Stmt):

	def __init__(self, statements):
		self.statements = statements

	def accept(self, visitor):
		return visitor.visit_block_stmt(self)

class Expression(Stmt):

	def __init__(self, expression):
		self.expression = expression

	def accept(self, visitor):
		return visitor.visit_expression_stmt(self)

class If(Stmt):

	def __init__(self, condition, then_branch, else_branch):
		self.condition = condition
		self.then_branch = then_branch
		self.else_branch = else_branch

	def accept(self, visitor):
		return visitor.visit_if_stmt(self)

class Print(Stmt):

	def __init__(self, expression):
		self.expression = expression

	def accept(self, visitor):
		return visitor.visit_print_stmt(self)

class Var(Stmt):

	def __init__(self, name, initializer):
		self.name = name
		self.initializer = initializer

	def accept(self, visitor):
		return visitor.visit_var_stmt(self)

