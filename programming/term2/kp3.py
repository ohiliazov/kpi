import math


class Dot:
    def __init__(self, x: [int, float], y: [int, float]):
        self.x = None
        self.y = None

        self.set_x(x)
        self.set_y(y)

    def set_x(self, x):
        if not isinstance(x, (int, float)):
            raise TypeError('Coordinate should be a number')
        self.x = x

    def set_y(self, y):
        if not isinstance(y, (int, float)):
            raise TypeError('Coordinate should be a number')
        self.y = y

    def angle(self, x, y):
        dy = y - self.y
        dx = x - self.x

        return math.atan2(dy, dx)


class Rhombus(Dot):
    def __init__(self, x: [int, float], y: [int, float], d1: [int, float], d2: [int, float]):
        super().__init__(x, y)
        self.d1 = None
        self.d2 = None

        self.set_d1(d1)
        self.set_d2(d2)

    def set_d1(self, d1):
        if not isinstance(d1, (int, float)):
            raise TypeError('Length should be a number')
        self.d1 = d1

    def set_d2(self, d2):
        if not isinstance(d2, (int, float)):
            raise TypeError('Length should be a number')
        self.d2 = d2


class Circle(Dot):
    def __init__(self, x: [int, float], y: [int, float], r: [int, float]):
        super().__init__(x, y)
        self.r = None

        self.set_radius(r)

    def set_radius(self, r):
        if not isinstance(r, (int, float)):
            raise TypeError('Radius should be a number')
        self.r = r


class InscribedRegularTriangle(Circle):
    def __init__(self, x: [int, float], y: [int, float], r: [int, float], v: Dot):
        super().__init__(x, y, r)
        self.v1 = None
        self.v2 = None
        self.v3 = None
        self.set_vertices(v)

    def is_on_circle(self, d: Dot):
        return math.isclose((d.x - self.x) ** 2 + (d.y - self.y) ** 2, self.r ** 2)

    def set_vertices(self, v: Dot):
        if not self.is_on_circle(v):
            raise ValueError("Dot is not on circle")

        self.v1 = v
        angle_1 = v.angle(self.x, self.y)

        angle_2 = angle_1 + math.pi / 3
        v2_x = math.cos(angle_2) * (v.x - self.x) - math.sin(angle_2) * (v.y - self.y) + self.x
        v2_y = math.sin(angle_2) * (v.x - self.x) - math.cos(angle_2) * (v.y - self.y) + self.y

        self.v2 = Dot(v2_x, v2_y)
        assert self.is_on_circle(self.v2)

        angle_3 = angle_1 + 2 * math.pi / 3
        v3_x = math.cos(angle_3) * (v.x - self.x) - math.sin(angle_3) * (v.y - self.y) + self.x
        v3_y = math.sin(angle_3) * (v.x - self.x) - math.cos(angle_3) * (v.y - self.y) + self.y

        self.v3 = Dot(v3_x, v3_y)
        assert self.is_on_circle(self.v3)
