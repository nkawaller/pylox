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

    def is_at_end():
        return current >= len(source)
