"""Script that generates expr.py"""

import sys

def define_type(lines, basename, classname, fields):
    """Write each expression class (flat class structure)"""

    lines.append(f"class {classname}({basename}):\n\n"
                 f"\tdef __init__(self, {fields}):\n")
    fields = fields.split(", ")
    for field in fields:
        name = field.split(" ")[0]
        lines.append(f"\t\tself.{name} = {name}\n")
    lines.append("\n")
    lines.append("\tdef accept(self, visitor):\n"
                 f"\t\treturn visitor.visit_{classname.lower()}_{basename.lower()}(self)"
                 "\n"
                 "\n")

def define_visitor(lines, basename, types):
    """Create abstract base class for visitor"""
    lines.append("class Visitor(ABC):\n\n")
    for expr_type in types:
        typename = expr_type.split(":")[0].strip()
        lines.append("\t@abstractmethod\n"
                    f"\tdef visit_{typename.lower()}_{basename.lower()}(self, {basename.lower()}):\n"
                     "\t\tpass\n\n")


def define_ast(output_dir, basename, types):
    """Generate code for syntax tree"""

    path = f"{output_dir}{basename.lower()}.py"
    with open(path, "w", encoding='utf-8') as ast:
        lines = [
            "\"\"\"Syntax tree that represents the Lox grammar\"\"\"",
            "\n",
            "\n",
            "from abc import ABC, abstractmethod",
            "\n",
            "\n",
            f"class {basename}(ABC):\n",
            "\n",
            "\t@abstractmethod\n",
            "\tdef accept(self, visitor):\n",
            "\t\tpass"
            "\n",
            "\n"
        ]
        define_visitor(lines, basename, types)
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
            "Assign   : name, value",
            "Binary   : left, operator, right",
            "Call     : callee, paren, arguments",
            "Get      : object, name",
            "Grouping : expression",
            "Literal  : value",
            "Logical  : left, operator, right",
            "Set      : object, name, value",
            "This     : keyword",
            "Unary    : operator, right",
            "Variable : name"
        ]
        stmt_list = [
            "Block      : statements",
            "Class      : name, methods",
            "Expression : expression",
            "Function   : name, params, body",
            "If         : condition, then_branch, else_branch",
            "Print      : expression",
            "Return     : keyword, value",
            "Var        : name, initializer",
            "While      : condition, body"
        ]
        define_ast(output_dir, "Expr", expr_list)
        define_ast(output_dir, "Stmt", stmt_list)


if __name__ == "__main__":
    main()
