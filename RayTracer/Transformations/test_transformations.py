import math
import unittest
from RayTracer.Transformations.transformations import *
from RayTracer.Features.features import *


class MyTestCase(unittest.TestCase):
    def test_translation(self):
        transform = identity_matrix().translations(5, -3, 2)
        inverse = transform.inverse()
        p = Point(-3, 4, 5)
        v = Vector(-3, 4, 5)
        self.assertEquals(transform.multiply(p), Point(2, 1, 7))
        self.assertEquals(inverse.multiply(p), Point(-8, 7, 3))
        self.assertEquals(transform.multiply(v), Vector(-3, 4, 5))

    def test_scaling(self):
        transform = identity_matrix().scaling(2, 3, 4)
        inverse = transform.inverse()
        p = Point(-4, 6, 8)
        v = Vector(-4, 6, 8)
        self.assertEquals(transform.multiply(p), Point(-8, 18, 32))
        self.assertEquals(transform.multiply(v), Vector(-8, 18, 32))
        self.assertEquals(inverse.multiply(p), Point(-2, 2, 2))

    def test_rotation(self):
        p = Point(0, 1, 0)
        p1 = Point(0, 0, 1)

        half_quarter_x = identity_matrix().rotation_x(math.pi / 4)
        half_quarter_y = identity_matrix().rotation_y(math.pi / 4)
        half_quarter_z = identity_matrix().rotation_z(math.pi / 4)

        full_quarter_x = identity_matrix().rotation_x(math.pi / 2)
        full_quarter_y = identity_matrix().rotation_y(math.pi / 2)
        full_quarter_z = identity_matrix().rotation_z(math.pi / 2)

        self.assertEquals(half_quarter_x.multiply(p), Point(0, math.sqrt(2) / 2, math.sqrt(2) / 2))
        self.assertEquals(full_quarter_x.multiply(p), Point(0, 0, 1))
        self.assertEquals(half_quarter_x.inverse().multiply(p), Point(0, math.sqrt(2) / 2, -math.sqrt(2) / 2))
        self.assertEquals(half_quarter_y.multiply(p1), Point(math.sqrt(2) / 2, 0, math.sqrt(2) / 2))
        self.assertEquals(full_quarter_y.multiply(p1), Point(1, 0, 0))
        self.assertEquals(half_quarter_z.multiply(p), Point(-math.sqrt(2) / 2, math.sqrt(2) / 2, 0))
        self.assertEquals(full_quarter_z.multiply(p), Point(-1, 0, 0))

    def test_chained_transformations(self):
        p = Point(1, 0, 1)
        transformation = identity_matrix().rotation_x(math.pi/2).scaling(5, 5, 5).translations(10, 5, 7)
        self.assertEquals(transformation.multiply(p), Point(15, 0, 7))


if __name__ == '__main__':
    unittest.main()
