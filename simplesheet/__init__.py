#!python3
"""Simple Stupid Spreadsheet Module

Encapsulate spreadsheet-like functions as native Python Objects.
"""


import collections
import re


class Expression:
    def evaluate(self, context, dependencies=None):
        "Compute the value of this Expression"
        raise NotImplementedError('Subclasses should implement this!')

    def __str__(self):
        raise NotImplementedError('Subclasses should implement this!')

    def get_dependencies(self):
        "Return the dependencies of this expression for change propagation"
        return set()

    def __add__(self, other):
        if isinstance(other, Expression):
            return Add(self, other)
        raise TypeError(f'Cannot Add({type(self)}, {type(other)})')

    def __sub__(self, other):
        if isinstance(other, Expression):
            return Sub(self, other)
        raise TypeError(f'Cannot Sub({type(self)}, {type(other)})')

    def __mul__(self, other):
        if isinstance(other, Expression):
            return Mul(self, other)
        raise TypeError(f'Cannot Mul({type(self)}, {type(other)})')

    def __truediv__(self, other):
        if isinstance(other, Expression):
            return Div(self, other)
        raise TypeError(f'Cannot Div({type(self)}, {type(other)})')

    def __pow__(self, other):
        if isinstance(other, Expression):
            return Pow(self, other)
        raise TypeError(f'Cannot Pow({type(self)}, {type(other)})')


class Cell(Expression):
    def __init__(self, name):
        self.name = name

    def evaluate(self, context, dependencies=None):
        if dependencies is not None:
            dependencies.add(self.name)
        return context.get(self.name, 0)

    def __str__(self):
        return f'Cell[{self.name}]'

    def get_dependencies(self):
        return {self.name}


class Const(Expression):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context, dependencies=None):
        return self.value

    def __str__(self):
        return str(self.value)

    def get_dependencies(self):
        return set()


class Assignment(Expression):
    def __init__(self, cell_name, expression):
        self.cell_name = cell_name
        self.expression = expression

    def evaluate(self, context, dependencies=None):
        context[self.cell_name] = self.expression
        return self.expression.evaluate(context, dependencies)

    def __str__(self):
        return f'{self.__class__.__name__}({self.cell_name}, {self.expression})'

    def get_dependencies(self):
        return self.expression.get_dependencies()


class Add(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context, dependencies=None):
        if dependencies is not None:
            dependencies.update(self.left.get_dependencies())
            dependencies.update(self.right.get_dependencies())
        return self.left.evaluate(context, dependencies) + self.right.evaluate(context, dependencies)

    def __str__(self):
        return f'Add({self.left}, {self.right})'

    def get_dependencies(self):
        return self.left.get_dependencies().union(self.right.get_dependencies())


class Sub(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context, dependencies=None):
        if dependencies is not None:
            dependencies.update(self.left.get_dependencies())
            dependencies.update(self.right.get_dependencies())
        return self.left.evaluate(context, dependencies) - self.right.evaluate(context, dependencies)

    def __str__(self):
        return f'Sub({self.left}, {self.right})'

    def get_dependencies(self):
        return self.left.get_dependencies().union(self.right.get_dependencies())


class Mul(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context, dependencies=None):
        if dependencies is not None:
            dependencies.update(self.left.get_dependencies())
            dependencies.update(self.right.get_dependencies())
        return self.left.evaluate(context, dependencies) * self.right.evaluate(context, dependencies)

    def __str__(self):
        return f'Mul({self.left}, {self.right})'

    def get_dependencies(self):
        return self.left.get_dependencies().union(self.right.get_dependencies())


class Div(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context, dependencies=None):
        if dependencies is not None:
            dependencies.update(self.left.get_dependencies())
            dependencies.update(self.right.get_dependencies())
        right_value = self.right.evaluate(context, dependencies)
        if right_value == 0:
            raise ZeroDivisionError('Division by zero')
        return self.left.evaluate(context, dependencies) / right_value

    def __str__(self):
        return f'Div({self.left}, {self.right})'

    def get_dependencies(self):
        return self.left.get_dependencies().union(self.right.get_dependencies())


class Pow(Expression):
    def __init__(self, base, exponent):
        self.base = base
        self.exponent = exponent

    def evaluate(self, context, dependencies=None):
        if dependencies is not None:
            dependencies.update(self.base.get_dependencies())
            dependencies.update(self.exponent.get_dependencies())
        return self.base.evaluate(context, dependencies) ** self.exponent.evaluate(context, dependencies)

    def __str__(self):
        return f'Pow({self.base}, {self.exponent})'

    def get_dependencies(self):
        return self.base.get_dependencies().union(self.exponent.get_dependencies())


class FloorDiv(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context, dependencies=None):
        if dependencies is not None:
            dependencies.update(self.left.get_dependencies())
            dependencies.update(self.right.get_dependencies())
        right_value = self.right.evaluate(context, dependencies)
        if right_value == 0:
            raise ZeroDivisionError('Division by zero')
        return self.left.evaluate(context, dependencies) // right_value

    def __str__(self):
        return f'FloorDif({self.base}, {self.exponent})'

    def get_dependencies(self):
        return self.base.get_dependencies().union(self.exponent.get_dependencies())


class Mod(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, context, dependencies=None):
        if dependencies is not None:
            dependencies.update(self.left.get_dependencies())
            dependencies.update(self.right.get_dependencies())
        return self.left.evaluate(context, dependencies) % self.right.evaluate(context, dependencies)

    def __str__(self):
        return f'Mod({self.left}, {self.right})'

    def get_dependencies(self):
        return self.left.get_dependencies().union(self.right.get_dependencies())


class Formula(Expression):
    "Allow existing python methods to be used in an expression"
    def __init__(self, func, *args):
        self.func = func
        self.args = args

    def evaluate(self, context, dependencies=None):
        if dependencies is not None:
            for arg in self.args:
                dependencies.update(arg.get_dependencies())
        evaluated_args = [arg.evaluate(context, dependencies) for arg in self.args]
        return self.func(*evaluated_args)

    def __str__(self):
        args_str = ', '.join(str(arg) for arg in self.args)
        return f'{self.__class__.__name__}({args_str})'

    def get_dependencies(self):
        deps = set()
        for arg in self.args:
            deps.update(arg.get_dependencies())
        return deps


class Canvas(collections.UserDict):
    def evaluate(self, cell_name=None):
        # TODO evaluate only dirty cells (based on dependencies)
        if cell_name:
            return self[cell_name].evaluate(self)

        retval = {}
        for key, val in self.items():
            retval[key] = val.evaluate(self) if isinstance(val, Expression) else val
        return retval

    def get_dependencies(self, cell_name=None):
        if cell_name:
            return self[cell_name].get_dependencies()

        retval = {}
        for key, val in self.items():
            retval[key] = val.get_dependencies() if isinstance(val, Expression) else val
        return retval

    def parse(self, s_expression):
        # This regex matches parentheses and symbols/numbers
        tokens = list(re.findall(r'\(|\)|[^\s()]+', s_expression))

        if not tokens:
            raise SyntaxError('Unexpected EOF')

        expression = self._build_expression_tree(tokens)
        if isinstance(expression, Assignment):
            self[expression.cell_name] = expression.expression

        return expression


    def _build_expression_tree(self, tokens):
        if not tokens:
            raise SyntaxError('Unexpected EOF')

        token = tokens.pop(0)

        if token == '(':
            operator = tokens.pop(0)  # Get the operator

            if operator == '=':
                # special case the assignment operator
                # maybe it should return the value that was assigned?
                cell_name = tokens.pop(0)
                expression = self._build_expression_tree(tokens)
                tokens.pop(0)
                return Assignment(cell_name, expression)

            operands = []
            while tokens[0] != ')':
                operands.append(self._build_expression_tree(tokens))

            # Remove the closing parenthesis
            tokens.pop(0)

            # Create the appropriate expression based on the operator
            if operator == '+':
                return Add(*operands)
            elif operator == '-':
                return Sub(*operands)
            elif operator == '*':
                return Mul(*operands)
            elif operator == '/':
                return Div(*operands)
            elif operator == '%':
                return Mod(*operands)
            elif operator == '//':
                return FloorDiv(*operands)
            elif operator == '**':
                return Pow(*operands)
            else:
                raise SyntaxError(f'Unknown operator: {operator}')

        elif re.match(r'^\d+$', token):  # Check if it's a number
            return Const(int(token))
        else:  # Otherwise, it must be a cell
            return Cell(token)
