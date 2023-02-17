import os
import sys

class Lox:

    args = sys.argv[1:]

    @classmethod
    def main(cls):
        if len(cls.args) > 1:
            print("Usage: python3 Lox.py [script]")
            sys.exit(1)
        elif len(cls.args) == 1:
            cls.run_file(cls.args[0])
        else:
            cls.run_prompt()

    @classmethod
    def run_file(cls, file):
        with open(file, "r") as reader:
            print(reader.read())

    @classmethod
    def run_prompt(cls):
        print("running prompt")

if __name__ == '__main__':
    Lox.main()