#import parsing
#import sys

from symbol import *

List = list
Number = (int, float)

class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    def __init__(self, params=(), args=(), outer=None):
        # Bind param list to corresponding args, or single parm to list of args
        self.outer = outer
        if isa(params, Symbol):
            self.update({params:list(args)})
        else:
            if len(args) != len(params):
                raise TypeError('expected %s, given %s, '
                                % (to_string(params), to_string(args)))
            self.update(zip(params,args))
    def find(self, var):
        "Find the innermost Env where var appears."
        if var in self: return self
        elif self.outer is None: raise LookupError(var)
        else: return self.outer.find(var)

def is_pair(x): return x != [] and isa(x, list)
def cons(x, y): return [x]+y

def callcc(proc):
    "Call proc with current continuation; escape only"
    ball = RuntimeWarning("Sorry, can't continue this continuation any longer.")
    def throw(retval): ball.retval = retval; raise ball
    try:
        return proc(throw)
    except RuntimeWarning as w:
        if w is ball: return ball.retval
        else: raise w

def add_globals(self):
    "Add some Scheme standard procedures."
    import sys, math, cmath, operator as op
    self.update(vars(math))
    self.update(vars(cmath))
    self.update({
     '+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv,
     'not':op.not_,'>':op.gt, '<':op.lt, '>=':op.ge,
     '<=':op.le, '=':op.eq,'equal?':op.eq, 'eq?':op.is_,
     'length':len, 'cons':cons,'car':lambda x:x[0],
     'cdr':lambda x:x[1:], 'append':op.add,
     'list':lambda *x:list(x), 'list?': lambda x:isa(x,list),
     'null?':lambda x:x==[], 'symbol?':lambda x: isa(x, Symbol),
     'boolean?':lambda x: isa(x, bool), 'pair?':is_pair,
     'port?': lambda x:isa(x,file), 'apply':lambda proc,l: proc(*l),
     'eval':lambda x: eval(expand(x)), 'load':lambda fn: load(fn), 'call/cc':callcc,
     'open-input-file':open,'close-input-port':lambda p: p.file.close(),
     'open-output-file':lambda f:open(f,'w'), 'close-output-port':lambda p: p.close(),
     #'eof-object?':lambda x:x is eof_object, 'read-char':parsing.readchar,
     #'read':read, 'write':lambda x,port=sys.stdout:port.write(to_string(x)),
     'display':lambda x,port=sys.stdout:port.write(x if isa(x,str) else to_string(x))})
    return self

isa = isinstance

global_env = add_globals(Env())


if __name__ == '__main__':
    print(global_env.find("null?")["+"])
