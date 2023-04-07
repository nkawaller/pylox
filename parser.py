"""Parser Class"""

import expr
import lox
import tokentypes

class ParseError(Exception):
    pass

class Parser:
    """Recursive descent parser"""

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        """Initial method to kick off the parser"""

        try:
            self.expression()
        except ParseError:
            return None

    def expression(self):
        """The top rule of our top-down parser"""

        return self.equality()

    def equality(self):
        """Determine if we're looking at an equality expression"""

        expr = self.comparison()

        while self.match([tokentypes.TokenType.BANG_EQUAL,
                          tokentypes.TokenType.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            expr = expr.Binary(expr, operator, right)
        return expr

    def comparison(self):
        """Determine if we're looking at a comparison expression"""

        expr = self.term()
        while self.match([tokentypes.TokenType.GREATER,
                          tokentypes.TokenType.GREATER_EQUAL,
                          tokentypes.TokenType.LESS,
                          tokentypes.TokenType.LESS_EQUAL]):
            operator = self.previous()
            right = self.term()
            expr = expr.Binary(expr, operator, right)
        return expr

    def term(self):
        """Determine if we're looking at addition or subtraction"""

        expr = self.factor()
        while self.match([tokentypes.TokenType.MINUS,
                          tokentypes.TokenType.PLUS]):
            operator = self.previous()
            right = self.factor()
            expr = expr.Binary(expr, operator, right)
        return expr

    def factor(self):
        """Determine if we're looking at multiplication or division"""

        expr = self.unary()
        while self.match([tokentypes.TokenType.SLASH,
                          tokentypes.TokenType.STAR]):
            operator = self.previous()
            right = self.unary()
            expr = expr.Binary(expr, operator, right)
        return expr

    def unary(self):
        """Look at current token to see if its a unary expression 
        (! or -)
        """

        if self.match([tokentypes.TokenType.BANG,
                       tokentypes.TokenType.MINUS]):
            operator = self.previous()
            right = self.unary()
            return expr.Unary(operator, right)

        return self.primary()

    def primary(self):
        """If we haven't matched any of the other rules, then we're
        working with primary expressions (the highest precedence 
        level
        """

        if self.match([tokentypes.TokenType.FALSE]):
            return expr.Literal(False)
        if self.match([tokentypes.TokenType.TRUE]):
            return expr.Literal(True)
        if self.match([tokentypes.TokenType.NIL]):
            return expr.Literal(None)
        if self.match([tokentypes.TokenType.NUMBER,
                       tokentypes.TokenType.STRING]):
            return expr.Literal(self.previous().literal)
        if self.match([tokentypes.TokenType.LEFT_PAREN]):
            expr = self.expression()
            self.consume(tokentypes.TokenType.RIGHT_PAREN,
                         "Expect ')' after expression.")
            return expr.Grouping(expr)
        raise self.error(self.peek(), "Expect expression.")

    def match(self, types):
        """Check current token and consume it if theres a match

        :param types: array of tokens
        :return: boolean
        """

        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def consume(self, type, message):
        """Look for the closing paren and report error if some 
        other token is found
        """

        if self.check(type):
            self.advance()
        else:
            self.error(self.peek(), message)

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

        return self.peek().tokentype == tokentypes.TokenType.EOF

    def peek(self):
        """Return current token"""

        return self.tokens[self.current]

    def previous(self):
        """Returns previous token"""

        return self.tokens[self.current - 1]

    def error(self, token, message):
        """Report error if we see an unexpected token"""

        lox.Lox.error(token, message)
        return ParseError()

    def synchronize(self):
        """If we encounter an error, discard tokens until we find the
        beginning of the next statement
        """
        
        self.advance()

        while not self.is_at_end():
            if self.previous.type == tokentypes.TokenType.SEMICOLON:
                return

            token_type = self.peek().tokentype
            if token_type in {
                tokentypes.TokenType.CLASS,
                tokentypes.TokenType.FUN,
                tokentypes.TokenType.VAR,
                tokentypes.TokenType.FOR,
                tokentypes.TokenType.IF,
                tokentypes.TokenType.WHILE,
                tokentypes.TokenType.PRINT,
                tokentypes.TokenType.RETURN}:
                return
            
            self.advance()
