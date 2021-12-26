import sys

try:
    import alive_progress
except ModuleNotFoundError:
    print('Modeval Expression Gen Test requires module: alive_progress')
    sys.exit()

sys.path.append('../src')

import modeval
import random
import math
from math import sin, cos, tan, pi, e

from alive_progress import alive_bar


class Expression(object):
    OPS = ['+', '-', '*', '/']

    GROUP_PROB = 0.4

    MIN_NUM, MAX_NUM = -20, 20

    def __init__(self, maxNumbers, _maxdepth=None, _depth=0):
        """
        maxNumbers has to be a power of 2
        """
        if _maxdepth is None:
            _maxdepth = math.log(maxNumbers, 2) - 1

        if _depth < _maxdepth and random.randint(0, _maxdepth) > _depth:
            self.left = Expression(maxNumbers, _maxdepth, _depth + 1)
        elif random.random() < 0.1:
            self.left = random.choice(['pi', 'e'])
        else:
            self.left = random.randint(Expression.MIN_NUM, Expression.MAX_NUM)
            if self.left == 0: self.left = 1

        if _depth < _maxdepth and random.randint(0, _maxdepth) > _depth:
            self.right = Expression(maxNumbers, _maxdepth, _depth + 1)
        elif random.random() < 0.1:
            self.right = random.choice(['pi', 'e'])
        else:
            self.right = random.randint(Expression.MIN_NUM, Expression.MAX_NUM)
            if self.right == 0: self.right = 1

        self.grouped = random.random() < Expression.GROUP_PROB
        self.operator = random.choice(Expression.OPS)

    def __str__(self):
        s = '{0!s} {1} {2!s}'.format(self.left, self.operator, self.right)
        if self.grouped:
            return '({0})'.format(s)
        else:
            return s


expressions = []
with alive_bar(10000, title='Generating Expressions', stats=None, elapsed=None) as bar:
    for i in range(10000):
        bar()
        while True:
            expr = str(Expression(64))
            try:
                eval(expr)
            except ZeroDivisionError:
                continue

            new_expr = ''

            for i, c in enumerate(expr):
                nc = c
                if random.random() < 0.25 and c == '(':
                    nc = random.choice([' sin(', ' cos(', ' tan('])
                new_expr += nc

            expressions.append(new_expr)
            break

p = modeval.Parser(ruleset=modeval.scientific_ruleset)

with alive_bar(10000, title='Testing Expressions', stats=None, elapsed=None) as bar:
    for i, v in enumerate(expressions):
        eval_result = round(eval(v), 8)
        parser_result = p.eval(v)

        if eval_result != parser_result:
            raise Exception(f'Test Failed: {v}\nEval answer:{eval_result}\nParser answer:{parser_result}')
        bar()

print('\nALL TESTS PASSED!')
