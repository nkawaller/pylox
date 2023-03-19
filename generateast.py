"""Script that generates expr.py"""

def write_file():
    """Write the code"""

    with open("expr.py", "w", encoding='utf-8') as ast:
        lines = [
            "\"\"\"Syntax tree that represents the Lox grammar\"\"\"",
            "\n",
            "\n",
            "from abc import ABC",
            "\n",
            "\n",
            "class Expr(ABC):\n",
            "\t\"\"\"Expression base class\"\"\""
            "\n",
            "\n",
            "\tdef __init__(self, left, operator, right):\n",
            "\t\tself.left = left\n",
            "\t\tself.operator = operator\n",
            "\t\tself.right = right\n"
        ]
        ast.writelines(lines)

def main():
    """Script entry point"""

    write_file()

if __name__ == "__main__":
    main()
