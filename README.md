# Seval

![](https://img.shields.io/badge/license-MIT-blue) ![](https://img.shields.io/badge/python-3.10-yellowgreen)

Seval (or Safe Eval) is a modular and secure string evaluation library that can be used to create custom parsers or interpreters.

### Basic Use

```python
from seval import Parser

# Create a new parser with the default ruleset.
p = Parser()

# Evalute string. Spaces are automatically removed.
print( p.eval('1 * (2-3)') )
```

### Rulesets 

The Parser class will use a basic mathematical ruleset if no specific ruleset is specified. Use the default ruleset as a guide on how to make custom ones.

```python
from seval import Parser, Ruleset

import operator # (standard library)

default_ruleset = Ruleset()

# Notice the order of the array follows order of operations.
default_ruleset.operators = [
    [('^', operator.pow), ('**', operator.pow)],
    [('*', operator.mul), ('/', operator.truediv)],
    [('+', operator.add), ('-', operator.sub)]
]

p = Parser(ruleset = default_ruleset)
```

Operator behavior is defined by the function attached to the sign/symbol in the tuple.

Note that the attached methods must have two inputs *in the correct order* (`L + R` is parsed as `add(L, R)`).

Seval also supports functions like `sin()`, but they are not included in the default ruleset. To add them, reference the following:

```python
from seval import Parser, Ruleset

import math # (standard library)

custom_ruleset = Ruleset()

# Function order does not matter, so an extra layer of grouping is not needed.
custom_ruleset.functions = [
    ('sin', math.sin),
    ('cos', math.cos),
    ('tan', math.tan)
]

p = Parser(ruleset = custom_ruleset)
# You can now use "sin(...)" in the input string for eval().
```

Speaking of `sin()`, what about `pi`? Seval also supports custom variables. They can be set like this:
```python
from seval import Parser, Ruleset

import math # (standard library)

custom_ruleset = Ruleset()

custom_ruleset.variables = [
    ('pi', math.pi) # Keep in mind this needs to be a value and not a function.
]

p = Parser(ruleset = custom_ruleset)
# Now you can use pi as you would expect (pi*3/2)
```

### Super Technical Limitations

If you're planning on doing something crazy with this library, I'd read this.

Multi-character operators and functions are assigned unicode characters while being processed so there is a limit of around 4000 variables (and also a very high upper limit of functions). If this is a problem you can increase the offset of the ***function*** unicode character conversion. Decreasing the offset of the operators runs the risk of an operator getting translated into a regular number.

A possible fix for this is automatically allocating unicode characters based on the number of operators and variables but this is not implemented as of now.