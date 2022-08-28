from unittest import TestCase

from iacopo.expars.calculator import Calculator


class SingleOperationTest(TestCase):
    def test_1(self):
        self.assertEqual(1, Calculator().calculate("1"))

    def test_minus_1(self):
        self.assertEqual(-1, Calculator().calculate("-1"))

    def test_plus1_1(self):
        self.assertEqual(2, Calculator().calculate("1+1"))

    def test_plus1_10(self):
        self.assertEqual(11, Calculator().calculate("1+10"))

    def test_plus10_10(self):
        self.assertEqual(20, Calculator().calculate("10+10"))

    def test_plus10_01(self):
        self.assertEqual(10.1, Calculator().calculate("10+0.10"))

    def test_minus1_1(self):
        self.assertEqual(0, Calculator().calculate("1-1"))

    def test_minus1_10(self):
        self.assertEqual(-9, Calculator().calculate("1-10"))

    def test_minus10_01(self):
        self.assertEqual(9.9, Calculator().calculate("10-0.10"))

    def test_mul2_3(self):
        self.assertEqual(6, Calculator().calculate("2*3"))

    def test_div2_3(self):
        self.assertAlmostEqual(0.666666, Calculator().calculate("2/3"), places=5)
