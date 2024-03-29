"""Entry point for the Lox language.

Use this class to run Lox programs via script or
interactive prompt.

Usage
-----
script : python3 lox.py <filename>
prompt : python3 lox.py
"""

import parser
import sys

from interpreter import Interpreter
from resolver import Resolver
from scanner import Scanner
from tokentypes import TokenType


class Lox:
    """Class used to run Lox"""

    args = sys.argv[1:]
    interpreter = Interpreter()
    had_error = False
    had_runtime_error = False

    @classmethod
    def main(cls):
        """Determine how user wants to run Lox

        :return: None
        """
        if len(cls.args) > 1:
            print("Usage: python3 Lox.py [script]")
            sys.exit(1)
        elif len(cls.args) == 1:
            cls.run_file(cls.args[0])
        else:
            cls.run_prompt()

    @classmethod
    def run_file(cls, path):
        """If user enters file name at the command line, open that
        file and read its contents

        :param path: location of file
        :return: None
        """
        try:
            with open(path, "r", encoding="utf-8") as reader:
                all_bytes = reader.read()
                cls.run(all_bytes)
                if cls.had_error:  # May need to adjust this
                    sys.exit(1)
                if cls.had_runtime_error:
                    sys.exit(1)
        except FileNotFoundError:
            print("Sorry, we could't find that file")

    @classmethod
    def run_prompt(cls):
        """Open repl so user can run Lox interactively

        :return: None
        """
        try:
            while True:
                line = input("> ")
                if line == ".exit":
                    sys.exit(0)
                cls.run(line)
                cls.had_error = False  # May need to adjust this

        except EOFError:
            print("\nUser entered control-d, exiting...")
        except KeyboardInterrupt:
            print("\nUser entered control-c, exiting...")

    @classmethod
    def run(cls, source):
        """Run the input through the scanner and print the tokens

        :param source: input from either file or interactive prompt
        :return: None
        """
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        prsr = parser.Parser(tokens)
        statements = prsr.parse()
        if cls.had_error:
            return
        resolver = Resolver(cls.interpreter)
        resolver.resolve(statements)
        if cls.had_error:
            return
        cls.interpreter.interpret(statements)

    @classmethod
    def error(cls, line, message):
        cls.report(line, " ", message)

    @classmethod
    def report(cls, line, where, message):
        print(f"[line {line}] Error {where} : {message}")

    @classmethod
    def parse_error(cls, token, message):
        if token.tokentype == TokenType.EOF:
            cls.report(token.line, "at end", message)
        else:
            cls.report(token.line, f" at '{token.lexeme}'", message)

    @classmethod
    def runtime_error(cls, error):
        print(f"{error.args} \n[line {error.token.line}]")
        cls.had_runtime_error = True


if __name__ == "__main__":
    Lox.main()
