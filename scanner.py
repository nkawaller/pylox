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

    # keywords = {
    #     "and":    TokenType.AND,
    #     "class":  TokenType.CLASS,
    #     "else":   TokenType.ELSE,
    #     "false":  TokenType.FALSE,
    #     "for":    TokenType.FOR,
    #     "fun":    TokenType.FUN,
    #     "if":     TokenType.IF,
    #     "nil":    TokenType.NIL,
    #     "or":     TokenType.OR,
    #     "print":  TokenType.PRINT,
    #     "return": TokenType.RETURN,
    #     "super":  TokenType.SUPER,
    #     "this":   TokenType.THIS,
    #     "true":   TokenType.TRUE,
    #     "var":    TokenType.VAR,
    #     "while":  TokenType.WHILE
    # }

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
    #     elif c == '/':
    #         if match('/'):
    #             while peek() is not '\n' and not self.is_at_end:
    #                 advance()
    #         else:
    #             self.add_token(SLASH)
    #         break
    #     elif c == ' ' or '\r' or '\t':
    #         break
    #     elif c == '\n':
    #         line += 1
    #         break
    #     elif c == '"':
    #         self.string()
    #         break
    #     else:
    #         if self.is_digit(c):
    #             self.number()
    #         elif self.is_alpha(c):
    #             self.identifier()
    #         else:
    #             Lox.error(self.line, "Unexpected character.")
    #         break

    # def identifier(self):
    #     while self.is_alpha_numeric(peek()):
    #         self.advance()
    #     # TODO: replace substring
    #     text = self.source.substring(self.start, self.current)
    #     type = self.keywords.get(text, None)
    #     if type is None:
    #         type = IDENTIFIER
    #     self.add_token(IDENTIFIER)

    # def number(self):
    #     while self.is_digit(self.peek()):
    #         self.advance()
    #     if self.peek() == '.' and self.is_digit(self.peek_next()):
    #         self.advance()

    #         while self.is_digit(self.peek()):
    #             self.advance()

    #     # TODO: Need to sort this out
    #     # should I just cast to a float?
    #     # the goal is to use python to convert the lexeme to a real double
    #     self.add_token(NUMBER, Double.parseDouble(source.substring(start, current)))

    # def string(self):
    #     while self.peek() is not '"' and not self.is_at_end():
    #         if self.peek() == '\n':
    #             line += 1
    #         self.advance()

    #     if self.is_at_end():
    #         Lox.error(self.line, "Undetermined string.");
    #         return

    #     self.advance()
    #     # TODO: probably handle substring with slice[:]
    #     # All it's doing anyway is stripping of the opening
    #     # and closing quotes
    #     value = self.source.substring(self.start + 1, self.current - 1)
    #     self.add_token(value)

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

    # def peek(self):
    #     """Lookahead method"""
    #     if self.is_at_end():
    #         return '\0'
    #     return self.source.charAt(self.current)

    # def peek_next(self):
    #     if self.current + 1 >= len(self.source()):
    #         return '\0'
    #     # TODO: find the charAt equivalent  
    #     return self.source.charAt(self.current + 1)

    # def is_alpha(self, c):
    #     return c >= 'a' and c <= 'z' or c >= 'A' and c <= 'Z' or c == '_'
    
    # def is_alpha_numeric(self, c):
    #     return self.is_alpha(c) or self.is_digit(c)

    # def is_digit(self, c):
    #     # Should these be integers instead of strings?
    #     return c >= '0' and c <= '9'

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        curr = self.source[self.current]
        self.current += 1
        return curr

    # def add_token(self, type):
    #     add_token(type, None)

    def add_token(self, type):
        text = self.source[self.start : self.current]
        self.tokens.append(token.Token(type, text, None, None))


    # def add_token(self, type, literal):
    #     text = self.source.substring(self.start, self.current)
    #     self.tokens.add(token.Token(type, text, literal, self.line))
