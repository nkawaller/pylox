import fileinput
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
    def run_file(cls, path):
        with open(path, "rb") as reader:
            all_bytes = reader.readline()
            cls.run(all_bytes)

    @classmethod
    def run_prompt(cls):
        for line in fileinput.input(encoding="utf-8"):
            cls.run(line)

    @classmethod
    def run(cls, source):
        print(source)


if __name__ == '__main__':
    Lox.main()