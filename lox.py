"""Entry point for the Lox language.

Use this class to run Lox programs via script or 
interactive prompt.

Usage
-----
script : python3 Lox.py <filename>
prompt : python3 Lox.py
"""
import sys
import scanner


class Lox:
    args = sys.argv[1:]
    had_error = False

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
        try:
            with open(path, "r") as reader:
                all_bytes = reader.read()
                cls.run(all_bytes)
                if cls.had_error:  # May need to adjust this
                    sys.exit(1)
        except FileNotFoundError:
            print("Sorry, we could't find that file")

    @classmethod
    def run_prompt(cls):
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
        s = scanner.Scanner(source)
        tokens = s.scan_tokens()
        # print(tokens)
        for token in tokens:
            print(str(token))

    @classmethod
    def error(cls, line, message):
        cls.report(line, " ", message)

    @classmethod
    def report(cls, line, where, message):
        print(f"[line {line}] Error {where} : {message}")


if __name__ == "__main__":
    Lox.main()
