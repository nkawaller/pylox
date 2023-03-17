"""Syntax tree that represents the Lox grammar"""

from abc import ABC

class Expr(ABC):

	def __init__(self, left, operator, right):
		self.left = left
		self.operator = operator
		self.right = right
