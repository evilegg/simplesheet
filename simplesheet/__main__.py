#!python3
"""Sample usage of a simplesheet
"""


from simplesheet import *
from simplesheet.formulas import Max, Min, Sum


if __name__ == "__main__":

    # Create a Spreadhsheet
    ss = Canvas({
        'A1': 5,
        'B1': 3,
        'C1': 2,
    })

    # Create the formula x = a + (b + 1) * (6 / c)
    ss['D1'] = Add(
        Cell('A1'),
        Mul(
            Add(Cell('B1'), Const(1)),
            Div(Const(6), Cell('C1'))
        )
    )

    # Example of using a built-in function (e.g., max)
    ss['E1'] = Max(Cell('A1'), Cell('B1'), Const(10))

    # Evaluate the formula and get dependencies
    result = ss.evaluate('D1')
    dependencies = ss.get_dependencies('D1')

    # Print the formula, its evaluated result, and dependencies
    print()
    print('Spreadsheet:', ss)
    print('Formula:', ss['D1'])
    print('Evaluated Result:', result)
    print('Dependencies:', dependencies)

    # Print the max formula, its evaluated result, and dependencies
    print()
    print('Max Formula:', ss['E1'])
    print('Max Evaluated Result:', ss.evaluate('E1'))
    print('Max Dependencies:', ss.get_dependencies('E1'))
    print()
    print('Sum Formula:', Sum(Cell('A1'), Cell('B1'), Const(10)))
    print('Sum Value:', Sum(Cell('A1'), Cell('B1'), Const(10)).evaluate(ss))
    print()
    print('Min Formula:', Min(Cell('A1'), Cell('B1'), Const(10)))
    print('Min Value:', Min(Cell('A1'), Cell('B1'), Const(10)).evaluate(ss))

    # Example of operator overloads to create a Formula
    ss['F1'] = Cell('A1') + (Cell('B1') + Const(1)) * (Const(6) / Cell('C1'))
    print()
    print('Implied Formula:', ss['F1'])
    print('Evaluated Result:', ss.evaluate('F1'))
    print('Dependencies:', ss.get_dependencies('F1'))

    print()
    print('Power: 3**2:', Const(3) ** Cell('C1'))
    print('Evaluated Result:', (Const(3) ** Cell('C1')).evaluate(ss))
    print('Dependencies:', (Const(3) ** Cell('C1')).get_dependencies())

    # Evaluate all of the formulas in the spreadsheet
    print()
    print('Evaluated Spreadsheet:', ss.evaluate())
    print('Computed Dependencies:', ss.get_dependencies())

    # Read from a string
    formula_string = '(+ A1 (* (+ B1 1) (/ 6 C1)))'
    print()
    print('Evaluate this string:', formula_string)
    print('Formula:', ss.parse(formula_string))
    print('Value:', ss.parse(formula_string).evaluate(ss))

    # Assignment from a string
    formula_string_with_assignment = '(= X1 (+ A1 (* (+ B1 1) (/ 6 C1))))'
    ss.parse(formula_string_with_assignment)
    print()
    print('Evaluate this string:', formula_string_with_assignment)
    print('Parsed:', ss['X1'])
    print('Value:', ss.evaluate('X1'))

