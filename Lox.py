class Lox:
    @staticmethod
    def main(*args):
        if len(args) > 1:
            print("Usage: pylox [script]")
        if len(args) == 1:
            print("running file")
            #runfile args[0]
        else:
            print("running prompt")
            #runprompt