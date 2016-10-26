def evaluate_list(operation, scope):
    if operation:
        for obj in operation:
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

    def accept(self, visitor):
        return visitor.visit_number(self)


class Function:

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        return evaluate_list(self.body, scope)


class FunctionDefinition:

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function

    def accept(self, visitor):
        return visitor.visit_function_definition(self)


class Conditional:
    def __init__(self, condtion, if_true, if_false=None):
        self.if_true = if_true
        self.if_false = if_false
        self.condtion = condtion

    def evaluate(self, scope):
        if self.condtion.evaluate(scope).value == 0:
            return evaluate_list(self.if_false, scope)
        else:
            return evaluate_list(self.if_true, scope)

    def accept(self, visitor):
        return visitor.visit_condtional(self)


class Print:

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        number = self.expr.evaluate(scope)
        print(number.evaluate(scope).value)
        return number

    def accept(self, visitor):
        return visitor.visit_print(self)


class Read:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        input_value = int(input())
        scope[self.name] = Number(input_value)
        return scope[self.name]

    def accept(self, visitor):
        return visitor.visit_read(self)


class FunctionCall:

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for arg_name, arg_val_expr in zip(function.args, self.args):
            call_scope[arg_name] = arg_val_expr.evaluate(scope)
        return function.evaluate(call_scope)

    def accept(self, visitor):
        return visitor.visit_function_call(self)


class Reference:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]

    def accept(self, visitor):
        return visitor.visit_reference(self)


class BinaryOperation:

    def __init__(self, lhs, op, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self, scope):
        left = self.lhs.evaluate(scope).value
        right = self.rhs.evaluate(scope).value
        op = self.op
        if op == '+':
            return Number(left + right)
        if op == '-':
            return Number(left - right)
        if op == '*':
            return Number(left * right)
        if op == '/':
            return Number(left // right)
        if op == '%':
            return Number(left % right)
        if op == '==':
            return Number(int(left == right))
        if op == '!=':
            return Number(int(left != right))
        if op == '<':
            return Number(int(left < right))
        if op == '>':
            return Number(int(left > right))
        if op == '>=':
            return Number(int(left >= right))
        if op == '<=':
            return Number(int(left <= right))
        if op == '&&':
            return Number(int(left and right))
        if op == '||':
            return Number(int(left or right))

    def accept(self, visitor):
        return visitor.visit_binary_operation(self)


class UnaryOperation:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        val = self.expr.evaluate(scope).value
        if self.op == '!':
            return Number(int(not val))
        if self.op == '-':
            return Number(-val)

    def accept(self, visitor):
        return visitor.visit_unary_operation(self)
