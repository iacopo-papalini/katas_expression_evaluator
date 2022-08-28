import unittest

from iacopo.expars import Operator, Number
from iacopo.expars.exceptions import UnexpectedTokenError, IncompleteExpressionError
from iacopo.expars.parser import Parser
from iacopo.expars.tokenizer import Tokenizer


class ParserTestCase(unittest.TestCase):
    def test_parse_trivial(self):
        tokens = Tokenizer("1+2").tokenize()
        operation = Parser(tokens).parse()
        self.assertEqual(Operator.PLUS, operation.operator)
        self.assertIsInstance(operation.left, Number)
        self.assertEqual(1, operation.left.evaluate())
        self.assertIsInstance(operation.right, Number)
        self.assertEqual(2, operation.right.evaluate())

    def test_parse_negative_number(self):
        tokens = Tokenizer("-.12").tokenize()
        number = Parser(tokens).parse()
        self.assertIsInstance(number, Number)
        self.assertEqual(-0.12, number.value)

    def test_weird(self):
        tokens = Tokenizer("--+-").tokenize()
        try:
            Parser(tokens).parse()
            raise AssertionError("Expected exception")
        except UnexpectedTokenError as e:
            self.assertEqual(1, e.position)
            self.assertEqual(
                "Unexpected token 'Operator.MINUS' at character 1", e.args[0]
            )

    def test_parse_sequence_1(self):
        tokens = Tokenizer("1+2-3").tokenize()
        operation = Parser(tokens).parse()
        self.assertEqual("1.0 2.0 3.0 - +", operation.as_polish())
        self.assertEqual(Operator.PLUS, operation.operator)
        self.assertEqual(1, operation.left.evaluate())
        minus = operation.right
        self.assertEqual(2, minus.left.evaluate())
        self.assertEqual(Operator.MINUS, minus.operator)
        self.assertEqual(3, minus.right.evaluate())

    def test_parse_sequence_2(self):
        tokens = Tokenizer("1*2+3").tokenize()
        operation = Parser(tokens).parse()
        self.assertEqual("1.0 2.0 * 3.0 +", operation.as_polish())
        self.assertEqual(Operator.PLUS, operation.operator)
        self.assertEqual(3, operation.right.evaluate())
        mul = operation.left
        self.assertEqual(1, mul.left.evaluate())
        self.assertEqual(Operator.MULTIPLY, mul.operator)
        self.assertEqual(2, mul.right.evaluate())

    def test_parse_paren(self):
        tokens = Tokenizer("1*(2+3)").tokenize()
        operation = Parser(tokens).parse()
        self.assertEqual("1.0 2.0 3.0 + *", operation.as_polish())

    def test_parse_paren_2(self):
        tokens = Tokenizer("(1+2)*3").tokenize()
        operation = Parser(tokens).parse()
        self.assertEqual("1.0 2.0 + 3.0 *", operation.as_polish())

    def test_parse_paren_broken(self):
        tokens = Tokenizer("(1+2)*3)").tokenize()
        try:
            Parser(tokens).parse()
            raise AssertionError("Expected exception")
        except UnexpectedTokenError as e:
            self.assertEqual(8, e.position)
            self.assertEqual("Unexpected token ')' at character 8", e.args[0])

    def test_parse_paren_broken_2(self):
        tokens = Tokenizer("(1+2))*3").tokenize()
        try:
            Parser(tokens).parse()
            raise AssertionError("Expected exception")
        except UnexpectedTokenError as e:
            self.assertEqual(6, e.position)
            self.assertEqual("Unexpected token ')' at character 6", e.args[0])

    def test_parse_paren_broken_3(self):
        tokens = Tokenizer("(1+2)300").tokenize()
        try:
            Parser(tokens).parse()
            raise AssertionError("Expected exception")
        except UnexpectedTokenError as e:
            self.assertEqual(8, e.position)
            self.assertEqual(
                "Unexpected token 'Number 300.0' at character 8", e.args[0]
            )

    def test_parse_paren_broken_4(self):
        tokens = Tokenizer("(1+2)*300+").tokenize()
        try:
            Parser(tokens).parse()
            raise AssertionError("Expected exception")
        except IncompleteExpressionError as e:
            self.assertEqual(
                "Missing symbol at the end of expression, last token parsed: Operator.PLUS at position 10",
                e.args[0],
            )
