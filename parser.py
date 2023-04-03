"""Parser Class"""

import expr
import tokentypes


class Parser:
    """Recursive descent parser"""

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def expression(self):
        """The top rule of our top-down parser"""

        return self.equality()

    def equality(self):
        """Determine if we're looking at an equality expression"""

        expr = self.comparison()

        while self.match(
                    tokentypes.TokenType.BANG_EQUAL,
                    tokentypes.TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = expr.Binary(expr, operator, right)
        return expr

    def comparison(self):
        """Determine if we're looking at a comparison expression"""

        expr = self.term()
        while self.match(
                    tokentypes.TokenType.GREATER,
                    tokentypes.TokenType.GREATER_EQUAL,
                    tokentypes.TokenType.LESS,
                    tokentypes.TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = expr.Binary(expr, operator, right)
        return expr

    def term(self):
        """Determine if we're looking at addition or subtraction"""

        expr = self.factor()
        while self.match(
                    tokentypes.TokenType.MINUS,
                    tokentypes.TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = expr.Binary(expr, operator, right)
        return expr

    def factor(self):
        """Determine if we're looking at multiplication or division"""

        expr = self.unary()
        while self.match(
                    tokentypes.TokenType.SLASH,
                    tokentypes.TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = expr.Binary(expr, operator, right)
        return expr

    def match(self, types):
        """Check current token and consume it if theres a match"""

        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type):
        """Look at the current token to see if it matches, but don't 
        consume it
        """

        if self.is_at_end():
            return False
        return self.peek().tokentype == type

    def advance(self):
        """Consume current token and return it"""

        if not self.is_at_end():
            self.current += 1
            return self.previous()

    def is_at_end(self):
        """Indicate when we've consumed all the tokens"""

        return self.peek().type == tokentypes.TokenType.EOF

    def peek(self):
        """Return current token"""

        return self.tokens[self.current]

    def previous(self):
        """Returnt previous token"""

        return self.tokens[self.current - 1]
