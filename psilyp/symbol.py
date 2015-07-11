class Symbol(str):
    pass


def Sym(s, symbol_table={}):
    "Find or create unique Symbol entry for str s in symbol table."
    if s not in symbol_table:
        symbol_table[s] = Symbol(s)

    return symbol_table[s]

_quote, _if, _set, _define, _lambda, _begin, = list(map(Sym,
"quote   if   set!  define   lambda   begin".split()))

_quasiquote, _unquote, _unquotesplicing = list(map(Sym,
"quasiquote   unquote   unquote-splicing".split()))

isa = isinstance


def to_string(x):
    "Convert a Python object back into a Lisp-readable string."
    if x is True:
        return "#t"
    elif x is False:
        return "#f"
    elif isa(x, Symbol):
        return x
    elif isa(x, str):
        return '"%s"' % x.encode('string_escape').replace('"', r'\"')
    elif isa(x, list):
        return '('+' '.join(list(map(to_string, x)))+')'
    elif isa(x, complex):
        return str(x).replace('j', 'i')
    else:
        return str(x)
