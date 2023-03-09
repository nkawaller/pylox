"""Scanner class"""

import lox
import tokentypes
import token

class Scanner:
    """The scanner consumes source code, groups lexemes together and
    outputs tokens
    """

    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    keywords = {
        "and":    tokentypes.TokenType.AND,
        "class":  tokentypes.TokenType.CLASS,
        "else":   tokentypes.TokenType.ELSE,
        "false":  tokentypes.TokenType.FALSE,
        "for":    tokentypes.TokenType.FOR,
        "fun":    tokentypes.TokenType.FUN,
        "if":     tokentypes.TokenType.IF,
        "nil":    tokentypes.TokenType.NIL,
        "or":     tokentypes.TokenType.OR,
        "print":  tokentypes.TokenType.PRINT,
        "return": tokentypes.TokenType.RETURN,
        "super":  tokentypes.TokenType.SUPER,
        "this":   tokentypes.TokenType.THIS,
        "true":   tokentypes.TokenType.TRUE,
        "var":    tokentypes.TokenType.VAR,
        "while":  tokentypes.TokenType.WHILE
    }

    def scan_tokens(self):
        """Take in the source code as a single string. Append tokens
        to the token list as we find them and return the list when 
        we're done.
        """

        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(token.Token(
                    tokentypes.TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        if c == '(':
            self.add_token(tokentypes.TokenType.LEFT_PAREN)
        elif c == ')':
            self.add_token(tokentypes.TokenType.RIGHT_PAREN)
        elif c == '{':
            self.add_token(tokentypes.TokenType.LEFT_BRACE)
        elif c == '}':
            self.add_token(tokentypes.TokenType.RIGHT_BRACE)
        elif c == ',':
            self.add_token(tokentypes.TokenType.COMMA)
        elif c == '.':
            self.add_token(tokentypes.TokenType.DOT)
        elif c == '-':
            self.add_token(tokentypes.TokenType.MINUS)
        elif c == '+':
            self.add_token(tokentypes.TokenType.PLUS)
        elif c == ';':
            self.add_token(tokentypes.TokenType.SEMICOLON)
        elif c == '*':
            self.add_token(tokentypes.TokenType.STAR)
        elif c == '!':
            self.add_token(tokentypes.TokenType.BANG_EQUAL 
                           if self.match('=') 
                           else tokentypes.TokenType.BANG)
        elif c == '=':
            self.add_token(tokentypes.TokenType.EQUAL_EQUAL 
                           if self.match('=') 
                           else tokentypes.TokenType.EQUAL)
        elif c == '<':
            self.add_token(tokentypes.TokenType.LESS_EQUAL 
                           if self.match('=') 
                           else tokentypes.TokenType.LESS)
        elif c == '>':
            self.add_token(tokentypes.TokenType.GREATER_EQUAL 
                           if self.match('=') 
                           else tokentypes.TokenType.GREATER)
        elif c == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.is_at_end:
                    self.advance()
            else:
                self.add_token(tokentypes.TokenType.SLASH)
        # elif c == ' ' or '\r' or '\t':
        #     return
        elif c == '\n':
            self.line += 1
        elif c == '"':
            self.string()
        else:
            if self.is_digit(c):
                self.number()
            elif self.is_alpha(c):
                self.identifier()
            else:
                lox.Lox.error(self.line, "Unexpected character.")

    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()
        text = self.source[self.start : self.current]
        type = self.keywords.get(text, None)
        if type is None:
            type = tokentypes.TokenType.IDENTIFIER
        self.add_token(tokentypes.TokenType.IDENTIFIER)

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        self.add_token(tokentypes.TokenType.NUMBER, 
                       float(self.source[self.start : self.current]))

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            lox.Lox.error(self.line, "Undetermined string.");
            return

        self.advance()
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(tokentypes.TokenType.STRING, value)

    def match(self, expected):
        """This method is like a conditional advance(). Once we see 
        the first part of the lexeme, we check to see if there's a 
        second part that we recognize. If there is, we know it's a 
        compound lexeme.
        """
        if self.is_at_end():
            return False
        if self.source[self.current] is not expected:
            return False
        self.current += 1
        return True

    def peek(self):
        """Lookahead method"""
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def is_alpha(self, c):
        return c >= 'a' and c <= 'z' or c >= 'A' and c <= 'Z' or c == '_'
    
    def is_alpha_numeric(self, c):
        return self.is_alpha(c) or self.is_digit(c)

    def is_digit(self, c):
        return c >= '0' and c <= '9'

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        curr = self.source[self.current]
        self.current += 1
        return curr

    def add_token(self, type, literal=None):
        text = self.source[self.start : self.current]
        self.tokens.append(token.Token(type, text, literal, None))
