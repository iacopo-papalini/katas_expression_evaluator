from unittest import TestCase

from iacopo.expars.calculator import Calculator


class MultiOperationTest(TestCase):
    def test_plus1_1_1(self):
        self.assertEqual(3, Calculator().calculate("1+1+1"))

    def test_mixed_plus_mul_1(self):
        self.assertEqual(17, Calculator().calculate("3*4+5"))
        self.assertEqual(17, Calculator().calculate("5+3*4"))

    def test_mixed_div_mul_1(self):
        self.assertEqual(12, Calculator().calculate("15*4/5"))
        self.assertEqual(2, Calculator().calculate("2*(3+4)/7"))

    def test_paren_1(self):
        self.assertEqual(27, Calculator().calculate("3*(4+5)"))
        self.assertEqual(32, Calculator().calculate("(5+3)*4"))

    def test_big(self):
        self.assertEqual(-70, Calculator().calculate("(8+9)/1-3*(4+5*(6-1))"))
