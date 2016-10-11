class Scope:

    def __init__(self, parent=None):
        self.parent = parent
        scope_dictionary = {}
        self.scope_dictionary = scope_dictionary

    def __getitem__(self, name):
        if self.scope_dictionary.get(name):
            return self.scope_dictionary[name]
        else:
            return self.parent[name]

    def __setitem__(self, name, val):
        self.scope_dictionary[name] = val


class Number:

    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self


class Function:

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        for obj in self.body:
            ev_result = obj.evaluate(scope)
        return ev_result


class FunctionDefinition:

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Conditional:
    def __init__(self, condtion, if_true, if_false=None):
        self.if_true = if_true
        self.if_false = if_false
        self.condtion = condtion

    def evaluate(self, scope):
        if self.condtion.evaluate(scope).value == 0:
            for obj in self.if_false:
                ev_result = obj.evaluate(scope)
            return ev_result
        else:
            for obj in self.if_true:
                ev_result = obj.evaluate(scope)
            return ev_result


class Print:

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        Number = self.expr.evaluate(scope)
        print(Number.evaluate(scope).value)
        return Number


class Read:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        input_value = int(input())
        scope[self.name] = Number(input_value)
        return scope[self.name]


class FunctionCall:

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for i in range(len(self.args)):
            call_scope[function.args[i]] = self.args[i].evaluate(call_scope)
        return function.evaluate(call_scope)


class Reference:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:

    def __init__(self, lhs, op, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self, scope):
        left = self.lhs.evaluate(scope).value
        right = self.rhs.evaluate(scope).value
        op = self.op
        if op == "+":
            return Number(left+right)
        if op == "-":
            return Number(left-right)
        if op == "*":
            return Number(left*right)
        if op == "/":
            return Number(left/right)
        if op == "%":
            return Number(left % right)
        if op == "==":
            return Number(int(left == right))
        if op == "!=":
            return Number(int(left != right))
        if op == "<":
            return Number(int(left < right))
        if op == ">":
            return Number(int(left > right))
        if op == ">=":
            return Number(int(left >= right))
        if op == "<=":
            return Number(int(left <= right))
        if op == "&&":
            return Number(int(left and right))
        if op == "||":
            return Number(int(left or right))


class UnaryOperation:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        val = self.expr.evaluate(scope).value
        if self.op == "!":
            if val:
                return Number(0)
            else:
                return Number(1)
        if self.op == "-":
            return Number(-val)


def example():
    parent = Scope()
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    parent["bar"] = Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    print('It should print 2: ', end=' ')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)


def my_tests():
    parent = Scope()
    parent["sign"] = Function(('a'),
                              [Conditional(BinaryOperation(Reference('a'),
                                                           '>=', Number(0)),
                                           [Number(1)], [Number(-1)])])
    parent["opposite"] = Function(('a', 'b'),
                                  [Conditional(BinaryOperation(Reference('a'),
                                                               '==',
                                                               UnaryOperation('-',
                                                                              Reference('b'))),
                                               [Number(1)], [Number(0)])])
    FunctionDefinition("average",
                       Function(('a', 'b'),
                                [BinaryOperation(BinaryOperation(Reference('a'),
                                                                 '+',
                                                                 Reference('b')),
                                                 '/',
                                                 Number(2))])).evaluate(parent)
    FunctionDefinition("max",
                       Function(('a', 'b'),
                                [Conditional(BinaryOperation(Reference('a'),
                                                             '>=',
                                                             Reference('b')),
                                             [Reference('a')],
                                             [Reference('b')])])).evaluate(parent)

    FunctionDefinition("factorial",
                       Function(('a'),
                                [Conditional(BinaryOperation(Reference('a'),
                                                             '<=',
                                                             Number(1)),
                                             [Reference('a')],
                                             [BinaryOperation(FunctionCall(Reference("factorial"),
                                                           [BinaryOperation(Reference('a'),
                                                                            '-',
                                                                            Number(1))]),
                                              "*",
                                              Reference('a'))])])).evaluate(parent)

    print('Должно вывести знак: ', end=' ')
    Print(FunctionCall(Reference("sign"), [Read("n")])).evaluate(parent)
    print('Должно вывести 1, если элементы обратные: ', end=' ')
    Print(FunctionCall(Reference("opposite"),
                       [Read('x'), Read('y')])).evaluate(parent)
    print('Должно вывести среднее арифметическое: ', end=' ')
    Print(FunctionCall(Reference("average"),
          [Read('x'), Read('y')])).evaluate(parent)
    print('Должно вывести максимум из двух чисел: ', end=' ')
    Read("x").evaluate(parent)
    Read("y").evaluate(parent)
    Print(FunctionCall(Reference("max"), [Reference('x'),
                                          Reference('y')])).evaluate(parent)
    print('Должно вывести знак среднего арифметического: ', end=' ')
    Print(FunctionCall(Reference("sign"), [FunctionCall(
        Reference("average"), [Read("t"), Read("p")])])).evaluate(parent)
    print('Должно вывести факториал числа: ', end=' ')
    Read("x").evaluate(parent)
    Print(FunctionCall(Reference("factorial"), [
        Reference("x")])).evaluate(parent)

if __name__ == '__main__':
    example()
    my_tests()
