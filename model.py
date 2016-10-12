def if_result(if_torf, scope):
    if if_torf:
        for obj in if_torf:
            ev_result = obj.evaluate(scope)
        return ev_result
    else:
        return None


class Scope:

    def __init__(self, parent=None):
        self.parent = parent
        self.scope_dict = {}

    def __getitem__(self, name):
        if name in self.scope_dict:
            return self.scope_dict[name]
        else:
            return self.parent[name]

    def __setitem__(self, name, val):
        self.scope_dict[name] = val


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
        if self.body:
            for obj in self.body:
                ev_result = obj.evaluate(scope)
            return ev_result
        else:
            return None


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
            return if_result(self.if_false, scope)
        else:
            return if_result(self.if_true, scope)


class Print:

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        number = self.expr.evaluate(scope)
        print(int(number.evaluate(scope).value))
        return number


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
        for f_obj, self_obj in zip(function.args, self.args):
            call_scope[f_obj] = self_obj.evaluate(scope)
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
            return Number(left + right)
        if op == "-":
            return Number(left - right)
        if op == "*":
            return Number(left * right)
        if op == "/":
            return Number(left // right)
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
            return Number(int(not val))
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
    F = Function
    FD = FunctionDefinition
    FC = FunctionCall
    BO = BinaryOperation
    R = Reference
    C = Conditional
    N = Number
    UO = UnaryOperation
    P = Print
    parent = Scope()
    parent["sign"] = F(('a'),
                       [C(BO(R('a'), '>=', N(0)),
                          [N(1)], [N(-1)])])
    parent["opposite"] = F(('a', 'b'),
                           [C(BO(R('a'), '==', UO('-', R('b'))),
                              [N(1)], [N(0)])])
    FD("average",
       F(('a', 'b'),
         [BO(BO(R('a'), '+', R('b')),
             '/', N(2))])).evaluate(parent)
    FD("max",
       F(('a', 'b'),
         [Conditional(BO(R('a'), '>=', R('b')),
          [R('a')],
          [R('b')])])).evaluate(parent)

    FD("factorial",
       F(('a'),
         [C(BO(R('a'), '<=', Number(1)),
            [R('a')],
            [BO(FC(R("factorial"),
                   [BO(R('a'), '-', N(1))]),
                "*", R('a'))])])).evaluate(parent)
    FD("ne_del_na_3",
       F(('a'),
         [C(BO(BO(R('a'), "%", N(3)), '==', N(0)),
            [], [Print(N(1))])])).evaluate(parent)
    FD("nothing", F(('a'), [])).evaluate(parent)
    FD("fib",
       F(('a'),
         [C(BO(R('a'), '<=', N(1)),
            [R('a')],
            [BO(FC(R('fib'),
                   [BO(R('a'), '-', N(1))]),
                '+', FC(R('fib'),
                        [BO(R('a'), '-', N(2))]))])])).evaluate(parent)
    FD('strange_max',
       F(('a', 'b'),
         [C(BO(R('a'), '<=', R('b')),
            [R('b')], [FC(R('strange_max'),
                          [R('b'), R('a')])])])).evaluate(parent)

    print('Должно вывести максимум из 2 чисел: ', end=' ')
    P(FC(R("strange_max"), [Read("n"), Read("k")])).evaluate(parent)
    print('Должно вывести число Фибоначчи данного номера: ', end=' ')
    P(FC(R("fib"), [Read("n")])).evaluate(parent)
    print('Должно вывести знак: ', end=' ')
    P(FC(R("sign"), [Read("n")])).evaluate(parent)
    print('Должно вывести 1, если элементы обратные: ', end=' ')
    P(FC(R("opposite"),
         [Read('x'), Read('y')])).evaluate(parent)
    print('Должно вывести среднее арифметическое: ', end=' ')
    P(FC(R("average"),
         [Read('x'), Read('y')])).evaluate(parent)
    print('Должно вывести максимум из двух чисел: ', end=' ')
    Read("x").evaluate(parent)
    Read("y").evaluate(parent)
    Print(FunctionCall(Reference("max"), [Reference('x'),
                                          Reference('y')])).evaluate(parent)
    print('Должно вывести знак среднего арифметического: ', end=' ')
    Print(FunctionCall(Reference("sign"),
                       [FunctionCall(Reference("average"),
                                     [Read("t"),
                                      Read("p")])])).evaluate(parent)
    print('Должно вывести факториал числа: ', end=' ')
    Read("x").evaluate(parent)
    Print(FunctionCall(Reference("factorial"), [
                       Reference("x")])).evaluate(parent)
    print('Должно вывести 1,если не делится на 3, и ничего иначе: ', end=' ')
    FC(R("ne_del_na_3"), [Read("x")]).evaluate(parent)
    print('Должно выполнить пустую функцию и не сломаться:) ', end=' ')
    FC(R('nothing'), [N(43)]).evaluate(parent)

if __name__ == '__main__':
    example()
    my_tests()
