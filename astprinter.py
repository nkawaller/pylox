import expr
import token
import tokentypes

class AstPrinter(expr.Expr):

    def __init__(self):
        pass

    def print_ast(self, expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme,
                            expr.left,
                            expr.right)

    def visit_grouping_expr(self, expr):
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr):
        if expr.value == None:
            return None
        return str(expr.value)

    def visit_unary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme,
                                 expr.right)


    def parenthesize(self, name, exprs):
        string = ""

        string += "(" + name
        for expr in exprs:
            string += " "
            string += (expr.accept(self))

        string += ")"

        return string

def main():
    printer = AstPrinter()
    expression = expr.Expr.Binary(
        expr.Expr.Unary(
            token.Token(tokentypes.TokenType.MINUS, "-", None, 1),
            expr.Expr.Literal(123),
            token.Token(tokentypes.TokenType.STAR, "*", None, 1),
            expr.Expr.Grouping(
                expr.Expr.Literal(45.67)
            )
        )
    )

    printer.print_ast(expression)


if __name__ == "__main__":
    main()
