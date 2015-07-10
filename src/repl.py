from parsing import InPort, parse, eof_object, to_string
from lisp_eval import lisp_eval
import sys


def repl(prompt='psylip> ', inport=InPort(sys.stdin), out=sys.stdout):
    "A prompt-read-eval-print loop."
    sys.stderr.write("psilyp version 1.0\n")
    while True:
        try:
            if prompt:
                print(prompt, sep="\n", end=" ")

            val = eval_string(inport)

            if val is eof_object:
                break

            if val is not None and out:
                print(val)

        except Exception as e:
            print ('%s: %s' % (type(e).__name__, e))


def eval_string(inport):
    "Eval string or inport"
    x = parse(inport)
    if x is eof_object:
        return x

    val = lisp_eval(x)
    if val is None:
        return None
    return to_string(val)


def load(filename):
    "Eval every expression from a file."
    repl(None, InPort(open(filename)), None)

if __name__ == '__main__':
    repl()
