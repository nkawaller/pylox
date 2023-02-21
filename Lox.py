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
        try:
            while True:
                line = input("> ")
                cls.run(line)
        except EOFError:
            print("\nReached end of file, closing prompt")
        except KeyboardInterrupt:
            print("\nClosing prompt...")

    @classmethod
    def run(cls, source):
        """
        Create a Scanner instance here:
            Scanner scanner = new Scanner(source);
            List<Token> tokens = scanner.scanTokens();
            for token in tokens:
                print(token)
        """
        print(source)


if __name__ == '__main__':
    Lox.main()