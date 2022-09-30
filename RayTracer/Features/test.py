import unittest
from features import Tuple

t1 = Tuple(1, 1, 1, 0)
t2 = Tuple(-1, 2, 7, 0)


class TestTuble(unittest.TestCase):
    def test_equality(self):
        self.assertFalse(t1 == t2)
        self.assertTrue(t1 == Tuple(1, 1, 1, 0))
        self.assertTrue(t1 != t2)

    def test_sum(self):
        self.assertEquals(t1 + t2, Tuple(0, 3, 8, 0))

    def test_subtraction(self):
        self.assertEquals(t1 - t2, Tuple(2, -1, -6, 0))

    def test_negation(self):
        self.assertEquals(-t2, Tuple(1, -2, -7, 0))
        self.assertEquals(-Tuple(6, -7, 8, 1), Tuple(-6, 7, -8, 1))


class TestVector(unittest.TestCase):
    def test_equality(self):
        self.assertFalse(t1 == t2)
        self.assertTrue(t1 == Tuple(1, 1, 1, 0))
        self.assertTrue(t1 != t2)


if __name__ == '__main__':
    unittest.main()
