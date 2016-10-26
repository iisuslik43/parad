from model import *
from folder import *


kolvo_otctupov = 0

def otc():
    for i in range(kolvo_otctupov):
            print('  ',end='')

class PrettyPrinter:

    def visit_arifm(self, tree):
        tree.accept(self)

    def visit(self, tree):
        otc()
        tree.accept(self)
        print(';')

    def visit_number(self, tree):
        print (tree.value, end='')

    def visit_condtional(self, tree):
        global kolvo_otctupov
        print('if(', end='')
        self.visit_arifm(tree.condtion)
        print('){')
        kolvo_otctupov+=1
        for statement in tree.if_true:
            self.visit(statement)
        kolvo_otctupov-=1
        otc()
        print('}', 'else', '{')
        kolvo_otctupov+=1
        for statement in tree.if_false:
            self.visit(statement)
        kolvo_otctupov-=1
        print('}', end='')

    def visit_read(self, tree):
        print('read ', end='')
        self.visit_arifm(tree.expr)

    def visit_function_definition(self, tree):
        global kolvo_otctupov
        print('def', tree.name, '(', end='')
        flag = False
        for arg in tree.function.args:
            if flag:
                print(',',end='')
            self.visit_arifm(arg)
            flag = True
        print('){')
        kolvo_otctupov+=1
        for statement in tree.function.body:
            self.visit(statement)
        kolvo_otctupov-=1
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
        flag = False
        for arg in tree.args:
            if flag:
                print(',', end='')
            self.visit_arifm(arg)
            flag = True
        print(')', end='')


def tests():
    printer = PrettyPrinter()
    con = Conditional(BinaryOperation(Number(43), '>', Number(42)),
                      [Print(UnaryOperation('-', Number(43))),
                       Print(Number(43))], [Print(Number(43)),
                                            Print(Number(43))])
    function = Function([Number(1),Number(2),Number(3)], [con])
    definition = FunctionDefinition('foo', function)
    printer = PrettyPrinter()
    printer.visit(definition)
    reference = Reference('foo')
    call = FunctionCall(reference, [Number(1), Number(2), Number(3)])
    printer = PrettyPrinter()
    printer.visit(call)
    printer.visit(Print(Number(43)))
    cond = Conditional(BinaryOperation(Number(43), '>', Number(42)), [Number(1)],[])
    printer.visit(cond)
    
    ff = ConstantFolder()
    printer.visit(ff.visit(Number(1)))
    printer.visit(ff.visit(cond))

if __name__ == "__main__":
    tests()
