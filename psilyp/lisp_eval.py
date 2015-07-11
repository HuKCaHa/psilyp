from env import *
from symbol import _quote, _if, _set, _define, _lambda, _begin


def lisp_eval(x, env=global_env):
    "lisp_evaluate an expression in an environment."
    while True:
        if isa(x, Symbol):       # variable reference
            return env.find(x)[x]
        elif not isa(x, list):   # constant literal
            return x
        elif x[0] is _quote:     # (quote exp)
            (_, exp) = x
            return exp
        elif x[0] is _if:        # (if test conseq alt)
            (_, test, conseq, alt) = x
            x = (conseq if lisp_eval(test, env) else alt)
        elif x[0] is _set:       # (set! var exp)
            (_, var, exp) = x
            env.find(var)[var] = lisp_eval(exp, env)
            return None
        elif x[0] is _define:    # (define var exp)
            (_, var, exp) = x
            env[var] = lisp_eval(exp, env)
            return None
        elif x[0] is _lambda:    # (lambda (var*) exp)
            (_, vars, exp) = x
            return Procedure(vars, exp, env)
        elif x[0] is _begin:     # (begin exp+)
            for exp in x[1:-1]:
                lisp_eval(exp, env)
            x = x[-1]
        else:                    # (proc exp*)
            exps = [lisp_eval(exp, env) for exp in x]
            proc = exps.pop(0)
            if isa(proc, Procedure):
                x = proc.exp
                env = Env(proc.parms, exps, proc.env)
            else:
                return proc(*exps)


class Procedure(object):
    "A user-defined Scheme procedure."
    def __init__(self, parms, exp, env):
        self.parms, self.exp, self.env = parms, exp, env

    def __call__(self, *args):
        return lisp_eval(self.exp, Env(self.parms, args, self.env))
