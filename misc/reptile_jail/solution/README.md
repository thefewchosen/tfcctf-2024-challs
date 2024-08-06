# Solution

The main problems with the blacklist is not allowing us to set variables using `=` nor calling functions unsing `()`. Both can be bypassed in a few different ways.

My solution used list comprehension to set variables

```python
[[a for a.__str__ in [print]] for a in [VARIABLE]]
# Equivalent to
VARIABLE.__str__ = print
```

For function calls we can overwrite class functions from the `help` variable

```python
[[a["Hello world"] for a.__class__.__getitem__ in [print]] for a in [help]][False][False]
# Equivalent to
print("Hello world")

[[-a for a.__class__.__neg__ in [print]] for a in [help]][False][False]
# Equivalent to
print()
```

After this, we can use various tricks to avoid the blacklist. My solution includes

- Using `True`/`False` to create numbers
- Using `help.__doc__` to get characters
- Calling `__add__` to concatenate strings

Script that creates a solution (very unoptimized) in `solve.py`