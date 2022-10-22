import unittest
from transformations import Matrix
from RayTracer.Features.features import *


class MyTestCase(unittest.TestCase):
    def test_constructor(self):
        rows = [[1, 2, 3.4], [4, 5, 6]]
        matrix = Matrix(2, 3, rows)
        self.assertEquals(matrix.rows, 2)
        self.assertEquals(matrix.get(0, 1), 2)
        matrix = Matrix(1, 5)
        self.assertEquals(matrix.get(0, 2), 0)

    def test_equality(self):
        rows = [[1, 2, 3.4], [4, 5, 6]]
        matrix = Matrix(2, 3, rows)
        matrix1 = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])
        self.assertFalse(matrix == matrix1)
        self.assertTrue(matrix == matrix)

    def test_neg(self):
        rows = [[1, 2, 3.4], [4, 5, 6]]
        matrix = Matrix(2, 3, rows)
        self.assertTrue(-matrix == Matrix(2, 3, [[-1, -2, -3.4], [-4, -5, -6]]))

    def test_multiplication(self):
        rows1 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]]
        rows2 = [[-2, 1, 2, 3], [3, 2, 1, -1], [4, 3, 6, 5], [1, 2, 7, 8]]
        matrix1 = Matrix(4, 4, rows1)
        matrix2 = Matrix(4, 4, rows2)
        matrix3 = matrix1.multiply(matrix2)

        rows3 = [[1, 2, 3, 4], [2, 4, 4, 2], [8, 6, 4, 1], [0, 0, 0, 1]]
        matrix4 = Matrix(4, 4, rows3)
        b = Tuple(1, 2, 3, 1)

        self.assertEquals(matrix3, Matrix(4, 4, [[20, 22, 50, 48], [44, 54, 114, 108], [40, 58, 110, 102],
                                                 [16, 26, 46, 42]]))
        c = matrix4.multiply(b)
        self.assertEquals(c, Tuple(18, 24, 33, 1))

    def test_transposition(self):
        matrix = Matrix(4, 4, [[0, 9, 3, 0], [9, 8, 0, 8], [1, 8, 5, 3], [0, 0, 5, 8]])
        matrix1 = Matrix(4, 4, [[0, 9, 1, 0], [9, 8, 8, 0], [3, 0, 5, 5], [0, 8, 3, 8]])
        self.assertTrue(matrix.transpose() == matrix1)

    def test_submatrix(self):
        matrix = Matrix(4, 4, [[-6, 1, 1, 6], [-8, 5, 8, 6], [-1, 0, 8, 2], [-7, 1, -1, 1]])
        sub_matrix = Matrix(3, 3, [[-6, 1, 6], [-8, 8, 6], [-7, -1, 1]])
        self.assertTrue(matrix.submatrix(2, 1) == sub_matrix)

    def test_determinant(self):
        m1 = Matrix(2, 2, [[1, 5], [-3, 2]])
        m2 = Matrix(3, 3, [[1, 2, 6], [-5, 8, -4], [2, 6, 4]])
        m3 = Matrix(4, 4, [[-2, -8, 3, 5], [-3, 1, 7, 3], [1, 2, -9, 6], [-6, 7, 7, -9]])

        self.assertEquals(m1.determinant(), 17)
        self.assertEquals(m2.determinant(), -196)
        self.assertEquals(m3.determinant(), -4071)

    def test_inverse(self):
        m = Matrix(4, 4, [[8, -5, 9, 2], [7, 5, 6, 1], [-6, 0, 9, 6], [-3, 0, -9, -4]])
        det = m.determinant()
        m_inverse = Matrix(4, 4, [[-0.15385, -0.15385, -0.28205, -0.53846],
                                  [-0.07692, 0.12308, 0.02564, 0.03077], [0.35897, 0.35897, 0.43590, 0.92308],
                                  [-0.69231, -0.69231, -0.76923, -1.92308]])
        i = m.inverse()
        self.assertTrue(m.inverse() == m_inverse)


if __name__ == '__main__':
    unittest.main()
