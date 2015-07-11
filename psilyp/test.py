import unittest
from repl import eval_string


class Test(unittest.TestCase):
    def test_add(self):
        self.assertEqual(eval_string("(+ 2 3)"), "5")

    def test_div(self):
        self.assertEqual(eval_string("(/ 4 2)"), "2.0")

    def test_define(self):
        eval_string("(define a 2)")
        self.assertEqual(eval_string("a"), "2")

    def test_define_func(self):
        eval_string("(define twice (lambda (x) (* 2 x)))")
        self.assertEqual(eval_string("(twice 5)"), "10")

    def test_lambdas(self):
        eval_string("(define twice (lambda (x) (* 2 x)))")
        eval_string("(define compose (lambda (f g) (lambda (x) (f (g x)))))")
        self.assertEqual(eval_string("((compose list twice) 5)"), "(10)")

    def test_large_numbers(self):
        eval_string("(define fact (lambda (n) (if (<= n 1) 1 (* n (fact (- n 1))))))")
        self.assertEqual(eval_string("(fact 50)"),
            "30414093201713378043612608166064768844377641568960512000000000000")

    def test_combine(self):
        eval_string("""(define combine (lambda (f)
    (lambda (x y)
      (if (null? x) (quote ())
          (f (list (car x) (car y))
             ((combine f) (cdr x) (cdr y)))))))""")
        eval_string("(define zip (combine cons))")
        self.assertEqual(eval_string("(zip (list 1 2 3 4) (list 5 6 7 8))"),
                                        "((1 5) (2 6) (3 7) (4 8))")

    def test_riff_shuffle(self):
        eval_string("""(define riff-shuffle (lambda (deck) (begin
    (define take (lambda (n seq) (if (<= n 0) (quote ()) (cons (car seq) (take (- n 1) (cdr seq))))))
    (define drop (lambda (n seq) (if (<= n 0) seq (drop (- n 1) (cdr seq)))))
    (define mid (lambda (seq) (/ (length seq) 2)))
    ((combine append) (take (mid deck) deck) (drop (mid deck) deck)))))""")
        self.assertEqual(eval_string("(riff-shuffle (list 1 2 3 4 5 6 7 8))"),
            "(1 5 2 6 3 7 4 8)")

    def test_quote(self):
        self.assertEqual(eval_string("(quote (testing 1 (2.0) -3.14e159))"),
            "(testing 1 (2.0) -3.14e+159)")

    def test_raise_syntax_error(self):
        with self.assertRaises(SyntaxError):
            eval_string("()")

        with self.assertRaises(SyntaxError):
            eval_string("(lambda 3 3)")

    def test_raise_type_error(self):

        with self.assertRaises(TypeError):
            eval_string("(define (twice x) (* 2 x))")

            eval_string("(twice 2 2)")

    def test_booleans(self):
        self.assertEqual(eval_string("(< 2 5)"), "#t")
        self.assertEqual(eval_string("(< 5 2)"), "#f")

    def test_quasiquote(self):
        eval_string("(define L (list 1 2 3))")
        self.assertEqual(eval_string("`(testing ,L testing)"), "(testing (1 2 3) testing)")

    def test_comments(self):
        self.assertEqual(eval_string("""'(1 ;test comments '
     ;skip this line
     2 ; more ; comments ; ) )
     3) ; final comment"""), "(1 2 3)")

    def test_set(self):
        eval_string("(define a 3)")
        eval_string("(set! a 4)")
        self.assertEqual(eval_string("a"), "4")

    def test_map(self):
        eval_string("(define (id x) x)")
        self.assertEqual(eval_string("(map id '(1 2 3 4))"), "(1 2 3 4)")

    def test_filter(self):
        eval_string("(define (lt5 x) (< x 5))")
        self.assertEqual(eval_string("(filter lt5 '(1 2 3 6 7))"), "(1 2 3)")

    def test_list(self):
        eval_string("(define L '(1 2 3 4))")
        self.assertEqual(eval_string("(car L)"), "1")
        self.assertEqual(eval_string("(cdr L)"), "(2 3 4)")
        self.assertEqual(eval_string("(length L)"), "4")

    def test_list2(self):
        eval_string("(define L1 '(1 2))")
        eval_string("(define L2 '(3 4))")
        self.assertEqual(eval_string("(append L1 L2)"), "(1 2 3 4)")
        self.assertEqual(eval_string("(cons  3 L2)"), "(3 3 4)")

    def test_null(self):
        self.assertEqual(eval_string("(null? '())"), "#t")
        self.assertEqual(eval_string("(null? '(1 2))"), "#f")

if __name__ == '__main__':
    unittest.main()
