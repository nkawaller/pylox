"""Parser Class"""

import expr
from lox import Lox
import stmt
from tokentypes import TokenType


class ParseError(Exception):
    pass


class Parser:
    """Recursive descent parser"""

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        """Initial method to kick off the parser"""

        statements = []
        try:
            while not self.is_at_end():
                statements.append(self.declaration())
            return statements
        except ParseError:
            return None

    def expression(self):
        """The top rule of our top-down parser"""

        return self.assignment()

    def declaration(self):
        try:
            if self.match([TokenType.CLASS]):
                return self.class_declaration()
            if self.match([TokenType.FUN]):
                return self.function("function")
            if self.match([TokenType.VAR]):
                return self.var_declaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None

    def class_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect a class name.")
        superclass = None
        if self.match([TokenType.LESS]):
            self.consume(TokenType.IDENTIFIER, "Expect a superclass name.")
            superclass = expr.Variable(self.previous())
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before class body.")
        methods = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            methods.append(self.function("method"))
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after class body.")
        return stmt.Class(name, superclass, methods)

    def statement(self):
        if self.match([TokenType.FOR]):
            return self.for_statement()
        if self.match([TokenType.IF]):
            return self.if_statement()
        if self.match([TokenType.PRINT]):
            return self.print_statement()
        if self.match([TokenType.RETURN]):
            return self.return_statement()
        if self.match([TokenType.WHILE]):
            return self.while_statement()
        if self.match([TokenType.LEFT_BRACE]):
            return stmt.Block(self.block())
        return self.expression_statement()

    def for_statement(self):
        """Method to parse for loops"""

        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
        initializer = None
        if self.match([TokenType.SEMICOLON]):
            initializer = None
        elif self.match([TokenType.VAR]):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()

        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condtion.")

        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body = self.statement()

        if increment is not None:
            body = stmt.Block([body, stmt.Expression(increment)])

        if condition is None:
            condition = expr.Literal(True)
        body = stmt.While(condition, body)

        if initializer is not None:
            body = stmt.Block([initializer, body])

        return body

    def if_statement(self):
        """Method to parse if-statements"""

        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.statement()
        else_branch = None
        if self.match([TokenType.ELSE]):
            else_branch = self.statement()

        return stmt.If(condition, then_branch, else_branch)

    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return stmt.Print(value)

    def return_statement(self):
        keyword = self.previous()
        value = None
        if not self.check([TokenType.SEMICOLON]):
            value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return stmt.Return(keyword, value)

    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name")
        initializer = None
        if self.match([TokenType.EQUAL]):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return stmt.Var(name, initializer)

    def while_statement(self):
        """Parse while statements"""

        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()
        return stmt.While(condition, body)

    def expression_statement(self):
        e = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return stmt.Expression(e)

    def function(self, kind):
        name = self.consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        self.consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(parameters) >= 255:
                    self.error(self.peek(), "Can't have more than 255 parameters.")
                parameters.append(
                    self.consume(TokenType.IDENTIFIER, "Expect parameter name.")
                )
                if not self.match([TokenType.COMMA]):
                    break
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LEFT_BRACE, f"Expect '{{' before {kind} body.")
        body = self.block()
        return stmt.Function(name, parameters, body)

    def block(self):
        """Group statement within a set of {} together"""

        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def assignment(self):
        """Determine if the = is being used to assign a value. This
        fn deals with the fact that we only have a single token
        lookahead and no backtracking
        """

        e = self.is_or()
        if self.match([TokenType.EQUAL]):
            equals = self.previous()
            value = self.assignment()

            if isinstance(e, expr.Variable):
                name = e.name
                return expr.Assign(name, value)
            if isinstance(e, expr.Get):
                get = e
                return expr.Set(get.object, get.name, value)

            self.error(equals, "Invalid assignment target")
        return e

    def is_or(self):
        """Parse 'or' expressions"""

        e = self.is_and()
        while self.match([TokenType.OR]):
            operator = self.previous()
            right = self.is_and()
            e = expr.Logical(e, operator, right)
        return e

    def is_and(self):
        """Parse 'and' expressions"""

        e = self.equality()
        while self.match([TokenType.AND]):
            operator = self.previous()
            right = self.equality()
            e = expr.Logical(e, operator, right)
        return e

    def equality(self):
        """Determine if we're looking at an equality expression"""

        e = self.comparison()

        while self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            e = expr.Binary(e, operator, right)
        return e

    def comparison(self):
        """Determine if we're looking at a comparison expression"""

        e = self.term()
        while self.match(
            [
                TokenType.GREATER,
                TokenType.GREATER_EQUAL,
                TokenType.LESS,
                TokenType.LESS_EQUAL,
            ]
        ):
            operator = self.previous()
            right = self.term()
            e = expr.Binary(e, operator, right)
        return e

    def term(self):
        """Determine if we're looking at addition or subtraction"""

        e = self.factor()
        while self.match([TokenType.MINUS, TokenType.PLUS]):
            operator = self.previous()
            right = self.factor()
            e = expr.Binary(e, operator, right)
        return e

    def factor(self):
        """Determine if we're looking at multiplication or division"""

        e = self.unary()
        while self.match([TokenType.SLASH, TokenType.STAR]):
            operator = self.previous()
            right = self.unary()
            e = expr.Binary(e, operator, right)
        return e

    def unary(self):
        """Look at current token to see if its a unary expression
        (! or -)
        """

        if self.match([TokenType.BANG, TokenType.MINUS]):
            operator = self.previous()
            right = self.unary()
            return expr.Unary(operator, right)

        return self.call()

    def finish_call(self, callee):
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(arguments) >= 255:
                    self.error(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())
                if not self.match([TokenType.COMMA]):
                    break
        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        return expr.Call(callee, paren, arguments)

    def call(self):
        """Determine if we're looking at a function call"""

        e = self.primary()
        while True:
            if self.match([TokenType.LEFT_PAREN]):
                e = self.finish_call(e)
            if self.match([TokenType.DOT]):
                name = self.consume(
                    TokenType.IDENTIFIER, "Expect property name after '.'."
                )
                e = expr.Get(e, name)
            else:
                break
        return e

    def primary(self):
        """If we haven't matched any of the other rules, then we're
        working with primary expressions (the highest precedence
        level
        """

        if self.match([TokenType.FALSE]):
            return expr.Literal(False)
        if self.match([TokenType.TRUE]):
            return expr.Literal(True)
        if self.match([TokenType.NIL]):
            return expr.Literal(None)
        if self.match([TokenType.NUMBER, TokenType.STRING]):
            return expr.Literal(self.previous().literal)
        if self.match([TokenType.SUPER]):
            keyword = self.previous()
            self.consume(TokenType.DOT, "Expect '.' after 'super'.")
            method = self.consume(
                TokenType.IDENTIFIER, "Expect superclass method name."
            )
            return expr.Super(keyword, method)
        if self.match([TokenType.THIS]):
            return expr.This(self.previous())
        if self.match([TokenType.IDENTIFIER]):
            return expr.Variable(self.previous())
        if self.match([TokenType.LEFT_PAREN]):
            e = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return expr.Grouping(e)
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
            return self.advance()
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

        return self.peek().tokentype == TokenType.EOF

    def peek(self):
        """Return current token"""

        return self.tokens[self.current]

    def previous(self):
        """Returns previous token"""
        return self.tokens[self.current - 1]

    def error(self, token, message):
        """Report error if we see an unexpected token"""

        Lox.parse_error(token, message)
        return ParseError()

    def synchronize(self):
        """If we encounter an error, discard tokens until we find the
        beginning of the next statement
        """

        self.advance()

        while not self.is_at_end():
            if self.previous().tokentype == TokenType.SEMICOLON:
                return

            token_type = self.peek().tokentype
            if token_type in {
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            }:
                return

            self.advance()
