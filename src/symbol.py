class Symbol(str): pass

def Sym(s, symbol_table={}):
    "Find or create unique Symbol entry for str s in symbol table."
    if s not in symbol_table:
        symbol_table[s] = Symbol(s)

    return symbol_table[s]

_quote, _if, _set, _define, _lambda, _begin, = list(map(Sym,
"quote   if   set!  define   lambda   begin".split()))

_quasiquote, _unquote, _unquotesplicing = list(map(Sym,
"quasiquote   unquote   unquote-splicing".split()))
