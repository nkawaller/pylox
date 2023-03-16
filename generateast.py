
def write_file():
    with open("expr.py", "w", encoding='utf-8') as ast:
        ast.write("class Expr:\n")
        ast.write("\n")
        ast.write("    def __init__(self):\n")
        ast.write("        pass")

def main():
    write_file()

if __name__ == "__main__":
    main()