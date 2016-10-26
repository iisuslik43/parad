from yat.model import *
from yat.folder import *


def print_statements(list_of_st, printer):
    if list_of_st:
        printer.indentation += 1
        for statement in list_of_st:
            printer.visit(statement)
        printer.indentation -= 1

def print_args(list_of_args, printer):
    flag = False
    for arg in list_of_args:
        if flag:
            print(',',end='')
        printer.visit_arifm(arg)
        flag = True

def print_indent(printer):
    for i in range(printer.indentation):
            print('  ',end='')

class PrettyPrinter:
    def __init__(self, indentation=None):
        self.indentation = indentation

    def visit_arifm(self, tree):
        tree.accept(self)

    def visit(self, tree):
        if not self.indentation:
            self.indentation = 0
        print_indent(self)
        tree.accept(self)
        print(';')

    def visit_number(self, tree):
        print (tree.value, end='')

    def visit_condtional(self, tree):
        print('if(', end='')
        self.visit_arifm(tree.condtion)
        print('){')
        print_statements(tree.if_true, self)
        print_indent(self)
        print('}', 'else', '{')
        print_statements(tree.if_false, self)
        print_indent(self)
        print('}', end='')

    def visit_read(self, tree):
        print('read ', tree.name, end='')

    def visit_function_definition(self, tree):
        print('def', tree.name, '(', end='')
        flag = False
        for arg in tree.function.args:
            if flag:
                print(',', end='')
            print(arg, end='')
            flag = True
        print('){')
        print_statements(tree.function.body, self)
        print_indent(self)
        print('}', end='')

    def visit_binary_operation(self, tree):
        print('(', end='')
        self.visit_arifm(tree.lhs)
        print(tree.op, end='')
        self.visit_arifm(tree.rhs)
        print(')', end='')

    def visit_unary_operation(self, tree):
        print('(', end='')
        print(tree.op, end='')
        self.visit_arifm(tree.expr)
        print(')', end='')

    def visit_reference(self, tree):
        print(tree.name, end='')

    def visit_print(self, tree):
        print('print ', end='')
        self.visit_arifm(tree.expr)

    def visit_function_call(self, tree):
        self.visit_arifm(tree.fun_expr)
        print('(', end='')
        print_args(tree.args, self)
        print(')', end='')


def tests():
    printer = PrettyPrinter()
    con = Conditional(BinaryOperation(Number(43), '>', Number(42)),
                      [Print(UnaryOperation('-', Number(43))),
                       Print(Number(43))], [Print(Number(43)),
                                            Print(Number(43))])
    function = Function(['a','b','c'], [con])
    definition = FunctionDefinition('foo', function)
    printer = PrettyPrinter()
    printer.visit(definition)
    deff = FunctionDefinition('sec', Function(['a'], [definition]))
    printer.visit(deff)
if __name__ == "__main__":
    tests()
