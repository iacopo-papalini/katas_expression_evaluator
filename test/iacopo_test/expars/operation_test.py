import unittest

from iacopo.expars import Operation, Operator, Number


class OperationTestCase(unittest.TestCase):
    def test_simple_minus(self):
        operation = Operation(Operator.MINUS, Number(5), Number(4))
        self.assertEqual(1, operation.evaluate())

    def test_simple_plus(self):
        operation = Operation(Operator.PLUS, Number(5), Number(4))
        self.assertEqual(9, operation.evaluate())

    def test_simple_mul(self):
        operation = Operation(Operator.MULTIPLY, Number(5), Number(4))
        self.assertEqual(20, operation.evaluate())

    def test_simple_divide(self):
        operation = Operation(Operator.DIVIDE, Number(5), Number(4))
        self.assertEqual(1.25, operation.evaluate())

    def test_recursion(self):
        operation = Operation(
            Operator.MINUS,
            Operation(Operator.MULTIPLY, Number(3), Number(4)),  # 12
            Operation(Operator.DIVIDE, Number(10), Number(2)),  # 5
        )
        # 12 - 5 = 7
        self.assertEqual(7, operation.evaluate())

    def test_precedence(self):
        plus = Operation(Operator.PLUS, Number(3), Number(4))
        divide = Operation(Operator.DIVIDE, Number(3), Number(4))
        minus = Operation(Operator.MINUS, Number(3), Number(4))
        mul = Operation(Operator.MULTIPLY, Number(3), Number(4))
        self.assertTrue(divide.has_precedence_over(plus))
        self.assertFalse(plus.has_precedence_over(divide))
        self.assertTrue(mul.has_precedence_over(minus))
        self.assertFalse(minus.has_precedence_over(divide))
        self.assertFalse(minus.has_precedence_over(plus))
        self.assertFalse(plus.has_precedence_over(minus))
        self.assertFalse(mul.has_precedence_over(divide))
        self.assertFalse(divide.has_precedence_over(mul))
