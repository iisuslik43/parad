from model import *

class PrettyPrinter:

    def visit(self, tree):
        tree.accept(self);

    def visit_first(self, tree):
        tree.accept(self);
        print(';')

    def visit_number(self, tree):
        print (tree.value, end = '')

    def visit_condtional(self, tree):
        print('if(', end = '')
        self.visit(tree.condtion)
        print('){')
        for statement in tree.if_true:
            print(end = '\t')
            self.visit(statement)
            print(';')
        print('}', 'else', '{')
        for statement in tree.if_false:
            print(end='\t')
            self.visit(statement)
            print(';')
        print('}', end='')

    def visit_read(self, tree):
        print('read ', end='')
        self.visit(tree.expr)

    def visit_function_definiction(self, tree):
        print('def (', end='')
        for arg in tree.function.args:
            self.visit(arg)
        print('){')
        for statement in tree.function.body:
            self.visit(statement)
            print(';')
        print('}', end = '')

    def visit_binary_operation(self, tree):
        print('(', end = '')
        self.visit(tree.lhs)
        print(tree.op, end = '')
        self.visit(tree.rhs)
        print(')', end = '')

    def visit_unary_operation(self, tree):
        print('(', end = '')
        print(tree.op, end = '')
        self.visit(tree.expr)
        print(')', end = '')

    def visit_reference(self, tree):
        print(tree.name, end='')

    def visit_print(self, tree):
        print('print ', end = '')
        self.visit(tree.expr)

    def visit_function_call(self, tree):
        self.visit(tree.fun_expr)
        print('(', end='')
        t=0;
        for arg in tree.args:
            if t:
                print(',', end='')
            self.visit(arg)
            t=1
        print(')', end='')

def tests():
    printer = PrettyPrinter()
    con = Conditional(BinaryOperation(Number(43), '>', Number(42)),
                      [Print(UnaryOperation('-', Number(43))),
                       Print(Number(43))], [Print(Number(43)),
                                           Print(Number(43))])
    function = Function([Number(1)], [con])
    definition = FunctionDefinition('foo', function)
    printer = PrettyPrinter()
    printer.visit_first(definition)
    reference = Reference('foo')
    call = FunctionCall(reference, [Number(1), Number(2), Number(3)])
    printer = PrettyPrinter()
    printer.visit_first(call)
    printer.visit_first(Print(Number(43)))
    
if __name__ == "__main__":
    tests()
