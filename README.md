# Mini DSL for spreadsheet like formulas

> Don't `eval()` a string, use a quirky DSL.

Inspired by a couple of conversations with a friend, I nerd-sniped myself into implementing a DSL for mathematical functions.
I had seen a similar syntax in the python-sqlalchemy module and I was wondering if something similar was possible for spreadsheet-like math formulas:

```python
ss = Canvas({
    'A1': 5,
    'B1': 3,
    'C1': 2,
})
ss['D1'] = Cell('A1') + (Cell('B1') + Const(1)) * (Const(6) / Cell('C1'))

# what does Cell('D1') equal?

print(ss['D1'])

# what does that formula evaluate to?

print(ss['D1'].evaluate())

# What does the value of the Cell at 'D1' depend upon?

print(ss['D1'].get_dependencies())
```

I've started with just the arithmetic operators, but we can also overload different operators to make DSL more robust:

- Comparison operators
- Assignment operators
- Bitwise operators
- Membership operators

## Running

The following will run a few examples:

```shell
$ python3 -m simplesheet
```
