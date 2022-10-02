import math


class Tuple:
    """
    An interface to represent either vectors or points
    """

    def __init__(self, x, y, z, w):
        # When w = 0 then the tuple is a vector else it is a point
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z and self.w == other.w

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return Tuple(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __sub__(self, other):
        return Tuple(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

    def __neg__(self):
        return Tuple(-self.x, -self.y, -self.z, self.w)

    def __str__(self):
        return '(' + self.x + ', ' + self.y + ', ' + self.z + ')'


class Vector(Tuple):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 0)

    def __mul__(self, other):
        return Vector(other * self.x, other * self.y, other * self.z)

    __rmul__ = __mul__

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other, self.z / other)

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        return self / self.magnitude()

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        x2 = self.y * other.z - self.z * other.y
        y2 = self.z * other.x - self.x * other.z
        z2 = self.x * other.y - self.y * other.x
        return Vector(x2, y2, z2)


class Point(Tuple):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 1)
