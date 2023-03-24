"""Syntax tree that represents the Lox grammar"""

from abc import ABC, abstractmethod

class Expr(ABC):
	pass

class Visitor(ABC):

	@abstractmethod
	def visitBinaryExpr(expr):
		pass

	@abstractmethod
	def visitGroupingExpr(expr):
		pass

	@abstractmethod
	def visitLiteralExpr(expr):
		pass

	@abstractmethod
	def visitUnaryExpr(expr):
		pass

class Binary(Expr):

	def __init__(self, left, operator, right):
		self.left = left
		self.operator = operator
		self.right = right

class Grouping(Expr):

	def __init__(self, expression):
		self.expression = expression

class Literal(Expr):

	def __init__(self, value):
		self.value = value

class Unary(Expr):

	def __init__(self, operator, right):
		self.operator = operator
		self.right = right

