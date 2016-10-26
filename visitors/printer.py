from yat.model import *
from yat.folder import *


class PrettyPrinter:

    def __init__(self, indentation=0):
        self.indentation = indentation

    def print_statements(self, list_of_st):
        if list_of_st:
            self.indentation += 1
            for statement in list_of_st:
                self.visit(statement)
            self.indentation -= 1

    def print_args(self, list_of_args):
        flag = False
        for arg in list_of_args:
            if flag:
                print(',', end='')
            self.visit_arithm(arg)
            flag = True

    def print_indent(self):
        for i in range(self.indentation):
            print('  ', end='')

    def visit_arithm(self, tree):
        tree.accept(self)

    def visit(self, tree):
        self.print_indent()
        tree.accept(self)
        print(';')

    def visit_number(self, tree):
        print(tree.value, end='')

    def visit_condtional(self, tree):
        print('if(', end='')
        self.visit_arithm(tree.condtion)
        print('){')
        self.print_statements(tree.if_true)
        self.print_indent()
        print('}', 'else', '{')
        self.print_statements(tree.if_false)
        self.print_indent()
        print('}', end='')

    def visit_read(self, tree):
        print('read ', tree.name, end='')

    def visit_function_definition(self, tree):
        print('def', tree.name, '(', end='')
        print(','.join(tree.function.args), end='')
        print('){')
        self.print_statements(tree.function.body)
        self.print_indent()
        print('}', end='')

    def visit_binary_operation(self, tree):
        print('(', end='')
        self.visit_arithm(tree.lhs)
        print(tree.op, end='')
        self.visit_arithm(tree.rhs)
        print(')', end='')

    def visit_unary_operation(self, tree):
        print('(', end='')
        print(tree.op, end='')
        self.visit_arithm(tree.expr)
        print(')', end='')

    def visit_reference(self, tree):
        print(tree.name, end='')

    def visit_print(self, tree):
        print('print ', end='')
        self.visit_arithm(tree.expr)

    def visit_function_call(self, tree):
        self.visit_arithm(tree.fun_expr)
        print('(', end='')
        self.print_args(tree.args)
        print(')', end='')


def tests():
    printer = PrettyPrinter()
    con = Conditional(BinaryOperation(Number(43), '>', Number(42)),
                      [Print(UnaryOperation('-', Number(43))),
                       Print(Number(43))], [Print(Number(43)),
                                            Print(Number(43))])
    function = Function(['a', 'b', 'c'], [con])
    definition = FunctionDefinition('foo', function)
    printer = PrettyPrinter()
    printer.visit(definition)
    deff = FunctionDefinition('sec', Function(['a'], [definition, definition]))
    printer.visit(deff)
if __name__ == "__main__":
    tests()
