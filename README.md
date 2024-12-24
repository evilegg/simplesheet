# Mini DSL for spreadsheet like formulas

> Don't `eval()` a string, use a quirky DSL.

Inspired by a couple of conversations with a friend, I nerd-sniped myself into implementing a DSL for mathematical functions.
I had seen similar in the python-sqlalchemy module and I was wondering if something similar was possible for spreadsheet-like math:

```python
Student = db.Table('Student', metadata, autoload=True, autoload_with=engine)
query = Student.update().values(Pass = True).where(Student.columns.Name == "Nisha")
results = conn.execute(query)
```

Spreadsheet-like math:

```python
ss = Canvas({
    'A1': 5,
    'B1': 3,
    'C1': 2,
})
ss['D1'] = Cell('A1') + (Cell('B1') + Const(1)) * (Const(6) / Cell('C1'))

# what does Cell('D1') equal?

print(ss['D1'].evaluate())
```

I've started with just the arithmetic operators, but we can also overload different operators to make DSL more robust:

- Comparison operators
- Assignment operators
- Bitwise operators
- Membership operators

