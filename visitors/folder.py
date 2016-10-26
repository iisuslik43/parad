from model import *


class ConstantFolder:
    def visit(self, tree):
        return tree.accept(self)

    def visit_number(self, tree):
        return tree

    def visit_condtional(self, tree):
        tree.condtion = self.visit(tree.condtion)
        for statement in tree.if_true:
            statement = self.visit(statement)
        for statement in tree.if_false:
            statement = self.visit(statement)
        return tree

    def visit_read(self, tree):
        return tree

    def visit_function_definition(self, tree):
        for statement in tree.function.body:
            self.visit(statement)
        return tree

    def visit_binary_operation(self, tree):
        if isinstance(tree.lhs, Number) and isinstance(tree.rhs, Number):
            return tree.evaluate(0)
        if tree.op == "*":
            if isinstance(tree.lhs, Reference) and isinstance(tree.rhs,Number) and tree.rhs.value == 0:
                return Number(0)
            if isinstance(tree.rhs, Reference) and isinstance(tree.lhs,Number) and tree.lhs.value == 0:
                return Number(0)
        if isinstance(tree.lhs, Reference) and isinstance(tree.rhs,Reference) and tree.lhs.name == tree.rhs.name:
            return Number(0)
        tree.lhs = self.visit(tree.lhs)
        tree.rhs = self.visit(tree.rhs)
        return tree

    def visit_unary_operation(self, tree):
        if isinstance(tree.expr, Number):
            return tree.evaluate(0)
        else:
            tree.expr = self.visit(tree.expr)
        return tree
        
    def visit_reference(self, tree):
        return tree

    def visit_print(self, tree):
        tree.expr = self.visit(tree.expr)
        return tree

    def visit_function_call(self, tree):
        for arg in tree.args:
            arg = self.visit(arg)
        return tree
