#!python3
"""Non-arithmetic formulas"""


from simplesheet import Formula


class Max(Formula):
    def __init__(self, *args):
        return Formula.__init__(self, max, *args)

    def __str__(self):
        args_str = ', '.join(str(arg) for arg in self.args)
        return f'{self.__class__.__name__}({args_str})'
