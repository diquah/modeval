import operator
import math


class Ruleset:
    def __init__(self):
        self.functions = []
        self.operators = []
        self.variables = []


default_ruleset = Ruleset()
default_ruleset.operators = [
    [('**', operator.pow)],
    [('*', operator.mul), ('/', operator.truediv)],
    [('+', operator.add), ('-', operator.sub)]
]

scientific_ruleset = Ruleset()
scientific_ruleset.operators = [
    [('^', operator.pow), ('**', operator.pow)],
    [('*', operator.mul), ('/', operator.truediv), ('%', operator.mod)],
    [('+', operator.add), ('-', operator.sub)],
]
scientific_ruleset.functions = [
    ('sin', math.sin),
    ('cos', math.cos),
    ('tan', math.tan),
]
scientific_ruleset.variables = [
    ('pi', math.pi),
    ('e', math.e),
]


# Used by parenthesis matching function.
def _push(obj, l, depth):
    while depth:
        l = l[-1]
        depth -= 1

    l.append(obj)


# Groups a string into nested arrays based on parenthesis in the input string.
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


class Parser:
    def __init__(self, ruleset: Ruleset = default_ruleset):
        self.ruleset = ruleset

        self.operator_filter = []
        self.operator_lookup = {}
        for op_layer in self.ruleset.operators:
            for op in op_layer:
                self.operator_filter.append(op[0])
                self.operator_lookup[op[0]] = op[1]

        self.function_filter = []
        self.function_lookup = {}
        for func in self.ruleset.functions:
            self.function_filter.append(func[0])
            self.function_lookup[func[0]] = func[1]

        self.variable_lookup = {}
        for var in self.ruleset.variables:
            self.variable_lookup[var[0]] = var[1]

    def _clean(self, grouped):
        cleaned = []
        num_buffer = ''
        op_buffer = ''
        char_buffer = ''
        for i, v in enumerate(grouped):
            if isinstance(v, str):
                if v in '1234567890.':
                    num_buffer += v
                elif num_buffer != '':
                    cleaned.append(float(num_buffer))
                    num_buffer = ''

                if v in self.operator_filter:
                    op_buffer += v
                elif op_buffer != '':
                    cleaned.append(op_buffer)
                    op_buffer = ''

                if v not in [*'1234567890.', *self.operator_filter]:
                    char_buffer += v
                elif char_buffer != '':
                    cleaned.append(char_buffer)
                    char_buffer = ''

            elif isinstance(v, list):
                if num_buffer != '':
                    cleaned.append(float(num_buffer))
                    num_buffer = ''
                if char_buffer != '':
                    cleaned.append(char_buffer)
                    char_buffer = ''
                if op_buffer != '':
                    cleaned.append(op_buffer)
                    op_buffer = ''

                cleaned.append(self._clean(v))

        if num_buffer != '':
            cleaned.append(float(num_buffer))
        if char_buffer != '':
            cleaned.append(char_buffer)
        if op_buffer != '':
            cleaned.append(op_buffer)

        return cleaned

    def _fill_vars(self, cleaned):
        filled = cleaned
        for i, v in enumerate(cleaned):
            if isinstance(v, list):
                filled[i] = self._fill_vars(v)
            else:
                if v in self.variable_lookup.keys():
                    filled[i] = self.variable_lookup[v]
                else:
                    filled[i] = v
        return filled

    # Applies an operator based on the symbol defined in the ruleset.
    def _operate(self, a, symbol, b):
        return self.operator_lookup[symbol](a, b)

    # Applies a function based on the string name defined in the ruleset.
    def _function(self, fun_name, a):
        return self.function_lookup[fun_name](a)

    # Reduces and simplifies nested arrays, numbers, operators, and functions recursively.
    def _calc(self, arr):
        for ops in self.operator_filter:
            i = 0
            a = None
            op = None
            negate = False
            while i < len(arr):
                if isinstance(arr[i], float):
                    if i - 1 >= 0:
                        if isinstance(arr[i - 1], float):
                            raise Exception('Expected operator in-between two numbers.')
                    if negate:
                        arr[i] *= -1
                        negate = False
                    if op is None:
                        a = arr[i]
                    else:
                        i -= 2
                        arr.pop(i)
                        arr.pop(i)
                        arr[i] = self._operate(a, op, arr[i])
                        a = arr[i]
                        op = None
                elif isinstance(arr[i], str):
                    if arr[i] == "-" and (i == 0 or isinstance(arr[i - 1], str) and arr[i - 1] in self.operator_filter):
                        negate = not negate
                        arr.pop(i)
                        i -= 1
                    elif arr[i] in ops:
                        op = arr[i]
                    elif arr[i] in self.function_filter:
                        if i + 1 < len(arr) and isinstance(arr[i + 1], list):
                            arr[i] = self._function(arr[i], self._calc(arr[i + 1]))
                            arr.pop(i + 1)
                            i -= 1
                        else:
                            raise Exception('Function was not supplied parameter.')
                elif isinstance(arr[i], list):
                    arr[i] = self._calc(arr[i])
                    i -= 1
                i += 1

        if len(arr) > 0:
            return arr[0]
        else:
            return None

    def eval(self, s):
        s = s.replace(' ', '')
        grouped = parse_parentheses(s)
        cleaned = self._clean(grouped)
        var_fill = self._fill_vars(cleaned)
        result = self._calc(var_fill)
        return result


def meval(input_str: str, ruleset: Ruleset = None):
    if ruleset is None:
        ruleset = default_ruleset
    temp_parser = Parser(ruleset=ruleset)
    return temp_parser.eval(input_str)


if __name__ == '__main__':
    p = Parser(ruleset=scientific_ruleset)
    try:
        while True:
            print(p.eval(input('>> ')))
            try:
                pass
            except KeyboardInterrupt:
                break
    except KeyboardInterrupt:
        pass