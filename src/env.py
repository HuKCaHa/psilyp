List = list         # A Lisp List -> a Python list
Number = (int, float)  # A Lisp Number -> a Python int or float


class Symbol(str):
    pass


def standard_env():
    '''An environment with some Lisp standard procedures.'''
    import math
    import operator as op
    env = Env()
    env.update(vars(math))  # sin, cos,etc
    env.update({
        '+': op.add, '-': op.sub,
        '*': op.mul, '//': op.floordiv, '/': op.truediv,
        '>': op.gt, '<': op.lt,
        '>=': op.ge, '<=': op.le, '=': op.eq,
        'abs':     abs,
        'append':  op.add,
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'eq?': op.is_,
        'equal?': op.eq,
        'length': len,
        'list': lambda *x: list(x),
        'list?': lambda x: isinstance(x, list),
        'map': map,
        'max': max,
        'min': min,
        'not': op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env


class Env(dict):
    '''An environment: a dict of {'var':val} pairs,
     with an outer Env.'''
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        "Find the innermost Env where var appears."

        if self.outer is None:
            return self if var in self else None

        return self if var in self else self.outer.find(var)

global_env = standard_env()  # will not be global for long

if __name__ == '__main__':
    print(global_env.find("a"))
