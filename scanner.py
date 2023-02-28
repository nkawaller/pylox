"""Scanner class"""

from lox import Lox
from tokentypes import TokenType
from token import Token

class Scanner:
    """Class that consumes source code, groups lexemes together
    and outputs tokens
    """

    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1


    def scan_tokens(self):
        while not self.is_at_end:
            start = self.current
            scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return tokens

    def scan_token(self):
        # TODO: May need this in a while loop, need an else at the end
        c = advance()
        if c == '(':
            add_token(LEFT_PAREN)
            break
        elif c == ')':
            add_token(RIGHT_PAREN)
            break
        elif c == '{':
            add_token(LEFT_BRACE)
            break
        elif c == '}':
            add_token(RIGHT_BRACE)
            break
        elif c == ',':
            add_token(COMMA)
            break
        elif c == '.':
            add_token(DOT)
            break
        elif c == '-':
            add_token(MINUS)
            break
        elif c == '+':
            add_token(PLUS)
            break
        elif c == ';':
            add_token(SEMICOLON)
            break
        elif c == '*':
            add_token(STAR)
            break
        elif c == '!':
            add_token(BANG_EQUAL if self.match('=') else BANG)
            break
        elif c == '=':
            add_token(EQUAL_EQUAL if self.match('=') else EQUAL)
            break
        elif c == '<':
            add_token(LESS_EQUAL if self.match('=') else LESS)
            break
        elif c == '>':
            add_token(GREATER_EQUAL if self.match('=') else GREATER)
            break
        elif c == '/':
            if match('/'):
                while peek() is not '\n' and not self.is_at_end:
                    advance()
            else:
                self.add_token(SLASH)
            break
        else:
            Lox.error(self.line, "Unexpected character.")
            break

    def match(self, expected):
        """Like a conditional advance()"""
        if self.is_at_end():
            return False
        if self.source.charAt(self.current) is not expected:
            return False
        self.current += 1
        return True

    def peek(self):
        """Lookahead method"""
        if self.is_at_end():
            return '\0'
        return self.source.charAt(self.current)

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        # charAt looks at a string, and gives you the char for the
        # index you provide
        return self.source.charAt(self.current += 1)

    def add_token(self, type):
        add_token(type, None)

    def add_token(self, type, literal):
        text = self.source.substring(self.start, self.current)
        self.tokens.add(Token(type, text, literal, self.line))
