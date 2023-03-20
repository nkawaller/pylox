"""Script that generates expr.py"""

import sys


def define_type(lines, basename, classname, fields):
    """Write each expression class"""

    lines.append(f"\tclass {classname}({basename}):\n\n"
                 f"\t\tdef __init__(self, {fields}):\n")
    fields = fields.split(", ")
    for field in fields:
        name = field.split(" ")[0]
        lines.append(f"\t\t\tself.{name} = {name}\n")
    lines.append("\n")


def define_ast(output_dir, basename, types):
    """Generate code for syntax tree"""

    path = f"{output_dir}{basename.lower()}.py"
    with open(path, "w", encoding='utf-8') as ast:
        lines = [
            "\"\"\"Syntax tree that represents the Lox grammar\"\"\"",
            "\n",
            "\n",
            "from abc import ABC",
            "\n",
            "\n",
            f"class {basename}(ABC):\n",
            "\n"
        ]
        for expr_type in types:
            classname = expr_type.split(":")[0].strip()
            fields = expr_type.split(":")[1].strip()
            define_type(lines, basename, classname, fields)
        ast.writelines(lines)


def main():
    """Script entry point"""
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: python3 generateast.py [output directory]")
        sys.exit(1)
    else:
        output_dir = args[0]
        expr_list = [
            # Could this be a dict?
            "Binary   : left, operator, right",
            "Grouping : expression",
            "Literal  : value",
            "Unary    : operator, right"
        ]
        define_ast(output_dir, "Expr", expr_list)


if __name__ == "__main__":
    main()
