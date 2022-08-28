from unittest import TestCase

from iacopo.expars import Operator, OpenParenthesis, ClosedParenthesis
from iacopo.expars.exceptions import NumberFormatError, UnexpectedTokenError
from iacopo.expars.tokenizer import Tokenizer


class TokenizerTest(TestCase):
    def test_plus_10_1_01(self):
        tokens = [_ for _ in Tokenizer("10+1.01").tokenize()]
        self.assertEqual(3, len(tokens))
        self.assertEqual(10, tokens[0].value)
        self.assertEqual(Operator.PLUS, tokens[1].operator)
        self.assertEqual(1.01, tokens[2].value)

    def test_plus_0_1_01(self):
        tokens = [_ for _ in Tokenizer("0+.01").tokenize()]
        self.assertEqual(3, len(tokens))
        self.assertEqual(0, tokens[0].value)
        self.assertEqual(Operator.PLUS, tokens[1].operator)
        self.assertEqual(0.01, tokens[2].value)

    def test_div_0_1_01(self):
        tokens = [_ for _ in Tokenizer("1/.01").tokenize()]
        self.assertEqual(3, len(tokens))
        self.assertEqual(1, tokens[0].value)
        self.assertEqual(Operator.DIVIDE, tokens[1].operator)
        self.assertEqual(0.01, tokens[2].value)

    def test_minus(self):
        tokens = [_ for _ in Tokenizer("-3.1415927").tokenize()]
        self.assertEqual(2, len(tokens))
        self.assertEqual(Operator.MINUS, tokens[0].operator)
        self.assertEqual(3.1415927, tokens[1].value)

    def test_paren(self):
        tokens = [_ for _ in Tokenizer("(3+4)*5").tokenize()]
        self.assertEqual(7, len(tokens))
        par1, _1, _2, _3, par2, _4, _5 = tokens
        self.assertIsInstance(par1, OpenParenthesis)
        self.assertIsInstance(par2, ClosedParenthesis)

    def test_error(self):
        try:
            _ = [_ for _ in Tokenizer("0.000.1").tokenize()]
            raise AssertionError("Expected Exception")
        except NumberFormatError as e:
            self.assertEqual(6, e.position)
            self.assertEqual("Unexpected '.'", e.message)

    def test_error_2(self):
        try:
            _ = [_ for _ in Tokenizer("0.000(1").tokenize()]
            raise AssertionError("Expected Exception")
        except UnexpectedTokenError as e:
            self.assertEqual(6, e.position)
            self.assertEqual("Unexpected token '(' at character 6", e.args[0])

    def test_weird(self):
        tokens = [_ for _ in Tokenizer("--+-").tokenize()]
        self.assertEqual(4, len(tokens))
