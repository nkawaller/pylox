"""Scanner class"""

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

    def scan_token():
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

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        return self.source.charAt(self.current += 1)

    def add_token(self, type):
        add_token(type, None)

    def add_token(self, type, literal):
        text = self.source.substring(self.start, self.current)
        self.tokens.add(Token(type, text, literal, self.line))
