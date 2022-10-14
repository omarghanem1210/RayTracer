import unittest
from features import *

t1 = Tuple(1, 1, 1, 0)
t2 = Tuple(-1, 2, 7, 0)

v1 = Vector(9, -7, 2.5)
v2 = Vector(10, 222, 65464)


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
    def test_scalar_multiplication(self):
        self.assertEquals(2 * v1, v1 * 2)
        self.assertEquals(2 * v1, Vector(18, -14, 5))

    def test_division(self):
        self.assertEquals(v1 / 2, Vector(4.5, -3.5, 1.25))

    def test_magnitude(self):
        self.assertEquals(v2.magnitude(), 65464.37718332009)

    def test_normalize(self):
        self.assertEquals(Vector(4, 0, 0).normalize(), Vector(1, 0, 0))

    def test_dot_product(self):
        self.assertEquals(Vector(1, 2, 3).dot(Vector(2, 3, 4)), 20)

    def test_cross_product(self):
        self.assertEquals(Vector(1, 2, 3).cross(Vector(2, 3, 4)), Vector(-1, 2, -1))
        self.assertEquals(Vector(2, 3, 4).cross(Vector(1, 2, 3)), Vector(1, -2, 1))


class TestColor(unittest.TestCase):
    def test_hadmard(self):
        c1 = Color(1, 0.2, 0.4)
        c2 = Color(0.9, 1, 0.1)
        self.assertEquals(c1.hadmard_product(c2), Color(0.9, 0.2, 0.04))


if __name__ == '__main__':
    unittest.main()
