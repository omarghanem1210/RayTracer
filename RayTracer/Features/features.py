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
