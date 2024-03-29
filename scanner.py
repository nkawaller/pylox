"""Scanner class"""

import tokenclass as token

import lox
from tokentypes import TokenType


class Scanner:
    """The scanner consumes source code, groups lexemes together with
    their types and outputs tokens
    """

    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    character_map = {
        "(": TokenType.LEFT_PAREN,
        ")": TokenType.RIGHT_PAREN,
        "{": TokenType.LEFT_BRACE,
        "}": TokenType.RIGHT_BRACE,
        ",": TokenType.COMMA,
        ".": TokenType.DOT,
        "-": TokenType.MINUS,
        "+": TokenType.PLUS,
        ";": TokenType.SEMICOLON,
        "*": TokenType.STAR,
        "!": lambda self: self.add_token(
            TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
        ),
        "=": lambda self: self.add_token(
            TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
        ),
        "<": lambda self: self.add_token(
            TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
        ),
        ">": lambda self: self.add_token(
            TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
        ),
        "/": lambda self: self.process_slash(),
        " ": lambda self: None,
        "\r": lambda self: None,
        "\t": lambda self: None,
        "\n": lambda self: setattr(self, "line", self.line + 1),
        '"': lambda self: self.string(),
    }

    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def scan_tokens(self):
        """Take in the source code as a single string. Append tokens
        to the token list as we find them and return the list when
        we're done.

        :return: list of tokens
        """

        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(token.Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        """Match the input character with its token type

        :return: None
        """
        c = self.advance()
        if c in self.character_map:
            if callable(self.character_map.get(c)):
                self.character_map[c](self)
            else:
                self.add_token(self.character_map.get(c), "None")
        elif c == '"':
            self.string()
        elif self.is_digit(c):
            self.number()
        elif self.is_alpha(c):
            self.identifier()
        else:
            lox.Lox.error(self.line, f"Unexpected character: {c}")

    def identifier(self):
        """Determine if character group is a reserved word, and if so,
        match to its keyword type

        :return: None
        """
        while self.is_alpha_numeric(self.peek()):
            self.advance()
        text = self.source[self.start:self.current]
        tokentype = self.keywords.get(text, None)
        if tokentype is None:
            tokentype = TokenType.IDENTIFIER
        self.add_token(tokentype)

    def number(self):
        """Convert numeric characters into python floats

        :return: None
        """
        while self.is_digit(self.peek()):
            self.advance()
        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def string(self):
        """Consume all characters between double quotes

        :return: Lox error if string doesn't have closing quote
        """
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            lox.Lox.error(self.line, "Undetermined string.")
            return

        self.advance()
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def match(self, expected):
        """This method is like a conditional advance(). Once we see
        the first part of the lexeme, we check to see if there's a
        second part that we recognize. If there is, we know it's a
        compound lexeme.

        :param expected:
        :return: boolean
        """
        if self.is_at_end():
            return False
        if self.source[self.current] is not expected:
            return False
        self.current += 1
        return True

    def peek(self):
        """Look ahead to next character

        :return: the next character
        """
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        """Look ahead two characters from current character

        :return: two characters ahead
        """
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def process_slash(self):
        """Determine if we're dealing with the divide-by symbol
        or a comment

        :return: None
        """
        if self.match("/"):
            while self.peek() != "\n" and not self.is_at_end:
                self.advance()
        else:
            self.add_token(TokenType.SLASH)

    def is_alpha(self, c):
        """Return true if a character is a letter

        :param c: current character
        :return: boolean
        """
        return "a" <= c <= "z" or "A" <= c <= "Z" or c == "_"

    def is_alpha_numeric(self, c):
        """Return true if a character is a letter or number

        :param c: current character
        :return: boolean
        """
        return self.is_alpha(c) or self.is_digit(c)

    def is_digit(self, c):
        """Return true if a character is a number

        :param c: current character
        :return: boolean
        """
        return "0" <= c <= "9"

    def is_at_end(self):
        """Return true when we've consumed all characters

        :return: boolean
        """
        return self.current >= len(self.source)

    def advance(self):
        """Consume the next character and return it

        :return: The next character in the input string
        """
        curr = self.source[self.current]
        self.current += 1
        return curr

    def add_token(self, tokentype, literal=None):
        """Once a character is matched, create a token and add to
        the token list

        :param type: identifies the lexeme type
        :param literal: TODO
        :return: None
        """
        text = self.source[self.start:self.current]
        self.tokens.append(token.Token(tokentype, text, literal, None))
