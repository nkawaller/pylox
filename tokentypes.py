"""Class of types to identify lexemes"""

from enum import Enum


class TokenType(Enum):
    """Names of token identifiers"""

    # Single-character tokens.
    LEFT_PAREN = "left paren"
    RIGHT_PAREN = "right paren"
    LEFT_BRACE = "left brace"
    RIGHT_BRACE = "right brace"
    COMMA = "comma"
    DOT = "dot"
    MINUS = "minus"
    PLUS = "plus"
    SEMICOLON = "semicolon"
    SLASH = "slash"
    STAR = "star"

    # One or two character tokens.
    BANG = "bang"
    BANG_EQUAL = "bang equal"
    EQUAL = "equal"
    EQUAL_EQUAL = "equal equal"
    GREATER = "greater"
    GREATER_EQUAL = "greater equal"
    LESS = "less"
    LESS_EQUAL = "less equal"

    # Literals
    IDENTIFIER = "identifier"
    STRING = "string"
    NUMBER = "number"

    # Keywords
    AND = "and"
    CLASS = "class"
    ELSE = "else"
    FALSE = "false"
    FUN = "fun"
    FOR = "for"
    IF = "if"
    NIL = "nil"
    OR = "or"
    PRINT = "print"
    RETURN = "return"
    SUPER = "super"
    THIS = "this"
    TRUE = "true"
    VAR = "var"
    WHILE = "while"

    EOF = "eof"
