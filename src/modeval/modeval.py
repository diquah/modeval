import operator
import math
from math import *

negative_char = chr(127)


def isnumeric(s: str):
    result = True
    for c in s:
        result = result and c in "0123456789."
    return result


# Used by parenthesis matching function.
def _push(obj, l, depth):
    while depth:
        l = l[-1]
        depth -= 1

    l.append(obj)


def parse_parentheses(s):
    groups = []
    depth = 0

    try:
        for char in s:
            if char == '(':
                _push([], groups, depth)
                depth += 1
            elif char == ')':
                depth -= 1
            else:
                _push(char, groups, depth)
    except IndexError:
        raise ValueError('Parentheses mismatch')

    if depth > 0:
        raise ValueError('Parentheses mismatch')
    else:
        return groups


class Ruleset:
    def __init__(self, operators=None, functions=None, constants=None):
        self.operators = operators or [
            {'^': operator.pow, '**': operator.pow},
            {'*': operator.mul, '/': operator.truediv, '%': operator.mod},
            {'+': operator.add, '-': operator.sub}
        ]
        self.functions = functions or {
            'math:sin': math.sin,
            'math:cos': math.cos,
            'math:tan': math.tan
        }
        self.constants = constants or {
            'math:pi': math.pi,
            'math:e': math.e
        }


class Parser:
    def __init__(self, ruleset):
        self.operators = ruleset.operators
        self.functions = ruleset.functions
        self.constants = ruleset.constants
        self.before_negative = set(c for opset in self.operators for k in opset.keys() for c in k)

    def _replace_chars(self, s: str):
        new = []
        for i, v in enumerate(s):
            if v == "-" and (i == 0 or s[i-1][-1] in self.before_negative):
                new.append(negative_char)
            else:
                new.append(v)
        return ''.join(new)

    def _group(self, arr: list):
        new_arr = []
        buffer = []
        mode = "number"
        for x in arr:
            # lists have to be recursively checked
            if isinstance(x, list):
                if len(buffer) > 0:
                    new_arr.append(''.join(buffer))
                    buffer = []
                new_arr.append(self._group(x))
                continue
            # change of mode
            elif mode == "number" and not isnumeric(x) or mode == "text" and not x.isalpha() or \
                    mode == "special" and (isnumeric(x) or x.isalpha()) or x == negative_char:
                if len(buffer) > 0:
                    new_arr.append(''.join(buffer))
                    buffer = []
                # set new mode
                if isnumeric(x):
                    mode = "number"
                elif x.isalpha():
                    mode = "text"
                else:
                    mode = "special"
            buffer.append(x)
        if len(buffer) > 0:
            new_arr.append(''.join(buffer))
        return new_arr

    def _eval(self, arr: list):
        # first pass over constants and recursive
        for i, v in enumerate(arr):
            if isinstance(v, list):
                arr[i] = self._eval(v)
            elif v in self.constants:
                arr[i] = self.constants[v]

        # second pass over functions and numbers
        i = 0
        negate = False
        while i < len(arr):
            v = arr[i]
            if v == negative_char:
                negate = True
                arr.pop(i)
                continue  # skip loop including increment
            elif isnumeric(v):
                arr[i] = float(v)
            elif isinstance(v, str) and v in self.functions:
                arr.pop(i)
                arr[i] = self.functions[v](arr[i])

            if negate and isinstance(arr[i], float):
                arr[i] = -arr[i]
                negate = False
            i += 1

        # third pass over operators
        for opset in self.operators:
            i = 0
            while i < len(arr):
                v = arr[i]
                if v == negative_char:
                    negate = True
                    arr.pop(i)
                    continue  # skip loop including increment
                elif v in opset:
                    i -= 1
                    a = arr.pop(i)
                    arr.pop(i)
                    arr[i] = opset[v](a, arr[i])
                    if negate:
                        arr[i] = -arr[i]
                        negate = False
                i += 1

        # hopefully there is only one number left
        return arr[0]

    def eval(self, s: str):
        s = ''.join(s.lower().split())
        replaced = self._replace_chars(s)
        organized = self._group(parse_parentheses(replaced))
        return self._eval(organized)


def meval(s: str, ruleset=Ruleset()):
    return Parser(ruleset).eval(s)


if __name__ == '__main__':
    p = Parser(ruleset=scientific_ruleset)
    try:
        while True:
            try:
                print(p.eval(input('>> ')))
            except KeyboardInterrupt:
                break
    except KeyboardInterrupt:
        pass