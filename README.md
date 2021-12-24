# modeval

![](https://img.shields.io/badge/license-MIT-blue) ![](https://img.shields.io/badge/python-3.10-yellowgreen)

Modeval (or Modular Eval) is a modular and secure string evaluation library that can be used to create custom parsers or interpreters.

Install using: `pip install modeval`

### Basic Use

If performance is not really a concern, you can use the `meval()` function.

```python
from modeval import meval

# Evalute string. Spaces are automatically removed.
print( meval('1 * (2-3)') )
```

Creating a parser class is more efficient for crunching lots of expressions with the same ruleset.

```python
from modeval import Parser

# Create a new parser with the default ruleset.
p = Parser()

# Evalute string. Spaces are automatically removed.
print( p.eval('1 * (2-3)') )
```



### Rulesets 

The Parser class will use a basic mathematical ruleset if no specific ruleset is specified. Use the default ruleset as a guide on how to make custom ones.

***Warning:*** You cannot change the ruleset of a parser once it has been initialized. Create a new parser instead.

```python
from modeval import Parser, Ruleset, meval

import operator # (standard library)

default_ruleset = Ruleset()

# Notice the order of the array follows order of operations.
default_ruleset.operators = [
    [('^', operator.pow), ('**', operator.pow)],
    [('*', operator.mul), ('/', operator.truediv)],
    [('+', operator.add), ('-', operator.sub)]
]

p = Parser(ruleset = default_ruleset)
meval('1+1', ruleset=default_ruleset) # Rulesets can also be supplied to meval()
```

Operator behavior is defined by the function attached to the sign/symbol in the tuple.

Note that the attached methods must have two inputs *in the correct order* (`L + R` is parsed as `add(L, R)`).

Modeval also supports functions like `sin()`, but they are not included in the default ruleset. To add them, reference the following:

```python
from modeval import Parser, Ruleset

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

Speaking of `sin()`, what about `pi`? Modeval also supports custom variables. They can be set like this:
```python
from modeval import Parser, Ruleset

import math # (standard library)

custom_ruleset = Ruleset()

custom_ruleset.variables = [
    ('pi', math.pi) # Keep in mind this needs to be a value and not a function.
]

p = Parser(ruleset = custom_ruleset)
# Now you can use pi as you would expect (pi*3/2)
```

### Technical Limitations

If you're planning on doing something crazy with this library, I'd read this.

Mult-character operators/variables/functions are assigned unique single unicode characters, meaning there is a limit for the amount of each you can have (around 4000 for each). This shouldn't be a problem in most cases.

A possible fix for this is dynamically allocating unicode characters, but this is not implemented yet.
