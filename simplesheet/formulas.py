#!python3
"""Non-arithmetic formulas"""


from simplesheet import Formula


class CustomFormula(Formula):
    def _calculate(self, *args):
        raise NotImplementedError('No method defined')

    def __init__(self, *args):
        return Formula.__init__(self, self._calculate, *args)


class Avg(CustomFormula):
    def _calculate(self, *args):
        return sum(args) / len(args)


class Max(CustomFormula):
    def _calculate(self, *args):
        return max(args)


class Min(CustomFormula):
    def _calculate(self, *args):
        return min(args)


class Sum(CustomFormula):
    def _calculate(self, *args):
        return sum(args)

