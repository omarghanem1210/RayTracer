import math

from RayTracer.Features.features import *


def intersections(*args):
    return sorted(list(args), key=lambda intersection: intersection.t)


def hit(l):
    t = Intersection(None, Sphere())
    for i in l:
        if t.t is None or 0 <= i.t <= t.t:
            t = i
    return t


def identity_matrix():
    m = Matrix(4, 4)
    for i in range(4):
        m.set(i, i, 1)
    return m


def lighting(material, light, point, eyev, normalv):
    effective_color = material.color.hadmard_product(light.intensity)
    lightv = (light.position - point)
    lightv = Vector(lightv.x, lightv.y, lightv.z)
    lightv = lightv.normalize()
    ambient = effective_color * material.ambient

    light_dot_normal = lightv.dot(normalv)
    if light_dot_normal < 0:
        diffuse = Color(0, 0, 0)
        specular = Color(0, 0, 0)
    else:
        diffuse = effective_color * material.diffuse * light_dot_normal

        reflectv = -lightv.reflect(normalv)
        reflect_dot_eye = reflectv.dot(eyev)
        if reflect_dot_eye <= 0:
            specular = Color(0, 0, 0)
        else:
            factor = math.pow(reflect_dot_eye, material.shininess)
            specular = light.intensity * material.specular * factor

    return ambient + diffuse + specular


class Matrix:
    def __init__(self, rows, columns, values=None):
        """The maximum number of rows and columns is 4,
        some methods may not work correctly if the matrix is not square"""
        self.rows = rows
        self.columns = columns
        self.values = values

        if self.values is None:
            self.values = []
            for i in range(rows):
                self.values.append([0] * columns)

        if len(self.values) != rows:
            raise ValueError('The number of rows does not the match the number in the entered matrix')

        for i in range(rows):
            if type(self.values[i]) != list and columns != 1:
                raise ValueError('The number of columns does not the match the number in the entered matrix')
        for i in range(rows):
            if columns == 1:
                break
            if len(self.values[i]) != columns:
                raise ValueError('The number of columns does not the match the number in the entered matrix')

    def get(self, y, x):
        """Returns the number at row y, column x"""
        return self.values[y][x]

    def set(self, y, x, value):
        self.values[y][x] = value

    def __eq__(self, other):
        if self.rows != other.rows or self.columns != other.columns:
            return False

        for i in range(self.rows):
            for j in range(self.columns):
                if not math.isclose(self.get(i, j), other.get(i, j), rel_tol=0.001, abs_tol=0.001):
                    return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __mul__(self, other):
        m = Matrix(self.rows, self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                m.set(i, j, self.get(i, j) * other)
        return m

    __rmul__ = __mul__

    def __neg__(self):
        return self.__mul__(-1)

    def multiply(self, other):
        """Multiplies two matrices or a matrix and a vector"""
        if issubclass(type(other), Tuple):
            if self.rows != 4:
                raise ValueError('number of columns does not match number of rows')
            else:
                m = Matrix(4, 1, [[other.x], [other.y], [other.z], [1]])
                m1 = self.multiply(m)
                if type(other) == Point:
                    return Point(m1.get(0, 0), m1.get(1, 0), m1.get(2, 0))
                elif type(other) == Vector:
                    return Vector(m1.get(0, 0), m1.get(1, 0), m1.get(2, 0))
                else:
                    return Tuple(m1.get(0, 0), m1.get(1, 0), m1.get(2, 0), m1.get(3, 0))

        if self.columns != other.rows:
            raise ValueError('number of columns does not match number of rows')

        m = Matrix(self.rows, other.columns)
        for i in range(m.rows):
            for j in range(m.columns):
                value = 0
                for k in range(self.columns):
                    value += self.get(i, k) * other.get(k, j)
                m.set(i, j, value)
        return m

    def transpose(self):
        """Returns the transpose of the matrix"""
        m = Matrix(self.columns, self.rows)

        for i in range(m.rows):
            for j in range(m.columns):
                m.set(i, j, self.get(j, i))
        return m

    def submatrix(self, x, y):
        """Returns the matrix after erasing row x, column y"""
        m = Matrix(self.rows - 1, self.columns - 1)

        for i in range(self.rows):
            row = i
            if i == x:
                continue
            if i > x:
                row = i - 1
            for j in range(self.columns):
                column = j
                if j == y:
                    continue
                if j > y:
                    column = j - 1
                m.set(row, column, self.get(i, j))
        return m

    def minor(self, x, y):
        """Returns the determinate of the submatrix at x and y"""
        sub_matrix = self.submatrix(x, y)
        return sub_matrix.determinant()

    def cofactor(self, x, y):
        return (-1) ** (x + y) * self.minor(x, y)

    def determinant(self):
        """Returns the determinant of a square matrix"""
        det = 0
        if self.rows == 2:
            det = self.get(0, 0) * self.get(1, 1) - self.get(0, 1) * self.get(1, 0)
        else:
            for column in range(self.columns):
                det += self.get(0, column) * self.cofactor(0, column)
        return det

    def inverse(self):
        """Returns the inverse of a matrix"""
        det = self.determinant()
        if det == 0:
            raise ValueError('this matrix is not invertible')

        m = Matrix(self.rows, self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                c = self.cofactor(i, j)
                m.set(j, i, c / det)
        return m

    def translations(self, x, y, z):
        m = Matrix(4, 4)
        k = 0
        for i in [x, y, z]:
            m.set(k, 3, i)
            m.set(k, k, 1)
            k += 1
        m.set(3, 3, 1)
        return m.multiply(self)

    def scaling(self, x, y, z):
        m = Matrix(4, 4)
        k = 0
        for i in [x, y, z, 1]:
            m.set(k, k, i)
            k += 1

        return m.multiply(self)

    def rotation_x(self, angle):
        m = identity_matrix()
        m.set(1, 1, math.cos(angle))
        m.set(1, 2, -math.sin(angle))
        m.set(2, 1, math.sin(angle))
        m.set(2, 2, math.cos(angle))
        return m.multiply(self)

    def rotation_y(self, angle):
        m = identity_matrix()
        m.set(0, 0, math.cos(angle))
        m.set(0, 2, math.sin(angle))
        m.set(2, 0, -math.sin(angle))
        m.set(2, 2, math.cos(angle))
        return m.multiply(self)

    def rotation_z(self, angle):
        m = identity_matrix()
        m.set(0, 0, math.cos(angle))
        m.set(0, 1, -math.sin(angle))
        m.set(1, 0, math.sin(angle))
        m.set(1, 1, math.cos(angle))
        return m.multiply(self)

    def shearing(self, x_y, x_z, y_x, y_z, z_x, z_y):
        m = identity_matrix()
        m.set(0, 1, x_y)
        m.set(0, 2, x_z)
        m.set(1, 0, y_x)
        m.set(1, 3, y_z)
        m.set(2, 0, z_x)
        m.set(2, 1, z_y)
        return m.multiply(self)


class Ray:
    def __init__(self, origin, direction):
        """Must have origin represented as a point and a direction represented as a vector"""
        self.origin = origin
        self.direction = direction

    def position(self, t):
        return self.origin + self.direction * t

    def intersect(self, s):
        ray = self.transform(s.transformation.inverse())
        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(ray.origin)
        c = ray.origin.dot(ray.origin) - 1
        discriminant = b * b - 4 * a * c

        if discriminant < 0:
            return []
        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        greater, smaller = max(t1, t2), min(t1, t2)
        return [Intersection(greater, s), Intersection(smaller, s)]

    def transform(self, t):
        new_origin = t.multiply(self.origin)
        new_direction = t.multiply(self.direction)
        return Ray(new_origin, new_direction)


class Material:
    def __init__(self, ambient=0.1, diffuse=0.9, specular=0.9, shininess=200, color=Color(1, 1, 1)):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.color = color


class Sphere:
    def __init__(self, transformation=identity_matrix(), sphere_material=Material()):
        """Represents a unit sphere centered at the origin"""
        self.transformation = transformation
        self.sphere_material = sphere_material

    def set_transformation(self, t):
        self.transformation = t

    def normal_at(self, world_point):
        object_normal = self.transformation.inverse().multiply(world_point)
        world_normal = self.transformation.inverse().transpose().multiply(object_normal)
        world_normal.w = 0
        return world_normal.normalize()


class Light:
    def __init__(self, position, intensity):
        self.intensity = intensity
        self.position = position


class Intersection:
    def __init__(self, t, obj):
        self.t = t
        self.obj = obj
