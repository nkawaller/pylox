"""Class of types to identify lexemes"""

from enum import Enum


class TokenType(Enum):
    """Names of token identifiers"""

    # Single-character tokens.
    LEFT_PAREN = (None,)
    RIGHT_PAREN = (None,)
    LEFT_BRACE = (None,)
    RIGHT_BRACE = (None,)
    COMMA = (None,)
    DOT = (None,)
    MINUS = (None,)
    PLUS = (None,)
    SEMICOLON = (None,)
    SLASH = (None,)
    STAR = (None,)

    # One or two character tokens.
    BANG = (None,)
    BANG_EQUAL = (None,)
    EQUAL = (None,)
    EQUAL_EQUAL = (None,)
    GREATER = (None,)
    GREATER_EQUAL = (None,)
    LESS = (None,)
    LESS_EQUAL = (None,)

    # Literals
    IDENTIFIER = (None,)
    STRING = (None,)
    NUMBER = (None,)

    # Keywords
    AND = (None,)
    CLASS = (None,)
    ELSE = (None,)
    FALSE = (None,)
    FUN = (None,)
    FOR = (None,)
    IF = (None,)
    NIL = (None,)
    OR = (None,)
    PRINT = (None,)
    RETURN = (None,)
    SUPER = (None,)
    THIS = (None,)
    TRUE = (None,)
    VAR = (None,)
    WHILE = (None,)

    EOF = None


