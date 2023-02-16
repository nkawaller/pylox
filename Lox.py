import os

class Lox:

    @classmethod
    def main(cls, *args):
        if len(args) > 1:
            print("Usage: pylox [script]")
        if len(args) == 1:
            cls.runfile(args[0])
        else:
            cls.run_prompt()


    @classmethod
    def run_file(cls, file):
        os.system(f"python3 {file}")

    @classmethod
    def run_prompt(cls):
        # Run prompt