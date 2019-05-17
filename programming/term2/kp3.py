import math
import matplotlib.pyplot as plt


class Point:
    def __init__(self, x: [int, float], y: [int, float]):
        self.set_x(x)
        self.set_y(y)

    def __str__(self):
        return f"Point({round(self.x, 2)}, {round(self.y, 2)})"

    @property
    def coordinates(self):
        return self.x, self.y

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


class Rhombus(Point):
    def __init__(self, x: [int, float], y: [int, float], d1: [int, float], d2: [int, float]):
        super().__init__(x, y)
        self.set_d1(d1)
        self.set_d2(d2)

    def __str__(self):
        return f"Rhombus(center={self.center}, diagonals={self.diagonals})"

    @property
    def coordinates(self):
        x, y, d1, d2 = self.x, self.y, self.d1, self.d2
        return (x + d1 / 2, y), (x, y + d2 / 2), (x - d1 / 2, y), (x, y - d2 / 2)

    @property
    def center(self):
        return self.coordinates

    @property
    def diagonals(self):
        return self.coordinates

    def set_d1(self, d1):
        if not isinstance(d1, (int, float)):
            raise TypeError('Length should be a number')
        self.d1 = d1

    def set_d2(self, d2):
        if not isinstance(d2, (int, float)):
            raise TypeError('Length should be a number')
        self.d2 = d2


class Circle(Point):
    def __init__(self, x: [int, float], y: [int, float], r: [int, float]):
        super().__init__(x, y)
        self.set_radius(r)

    def __str__(self):
        return f"Circle(center={str(self.center)}, radius={round(self.raduis, 2)})"

    @property
    def center(self):
        return self.coordinates

    def set_radius(self, r):
        if not isinstance(r, (int, float)):
            raise TypeError('Radius should be a number')
        self.raduis = r


class InscribedRegularTriangle(Circle):
    def __init__(self, x: [int, float], y: [int, float], r: [int, float], v: Point):
        super().__init__(x, y, r)
        self.set_vertices(v)

    def __str__(self):
        return f"InscribedRegularTriangle({[str(v) for v in self.vertices]})"

    @property
    def vertices(self):
        return self.v1, self.v2, self.v3

    def validate_point_on_circle(self, d: Point):
        if not math.isclose((d.x - self.x) ** 2 + (d.y - self.y) ** 2, self.raduis ** 2):
            raise ValueError("Dot is not on circle")

    def set_vertices(self, vertex: Point):
        self.validate_point_on_circle(vertex)

        dx = vertex.x - self.x
        dy = vertex.y - self.y

        # rotate initial vertex 120 degrees against center
        turn_angle = 2 * math.pi / 3
        v2_x = math.cos(turn_angle) * dx - math.sin(turn_angle) * dy + self.x
        v2_y = math.sin(turn_angle) * dx + math.cos(turn_angle) * dy + self.y

        vertex_2 = Point(v2_x, v2_y)
        self.validate_point_on_circle(vertex_2)

        # rotate initial vertex 240 degrees against center
        turn_angle = 4 * math.pi / 3
        v3_x = math.cos(turn_angle) * dx - math.sin(turn_angle) * dy + self.x
        v3_y = math.sin(turn_angle) * dx + math.cos(turn_angle) * dy + self.y

        vertex_3 = Point(v3_x, v3_y)
        self.validate_point_on_circle(vertex_3)

        self.v1 = vertex
        self.v2 = Point(v2_x, v2_y)
        self.v3 = Point(v3_x, v3_y)


if __name__ == '__main__':
    x, y, r = input('Enter X, Y, R of circle: ').split()
    x, y, r = float(x), float(y), float(r)
    fig_circle = Circle(x, y, r)
    print(fig_circle)

    circle = plt.Circle((x, y), r, color='red')
    _, ax = plt.subplots()
    ax.add_artist(circle)
    ax.set_xlim((x - 2 * r, x + 2 * r))
    ax.set_ylim((y - 2 * r, y + 2 * r))
    ax.set_aspect('equal')
    plt.title('Circle')
    plt.show()

    x, y, d1, d2 = input('Enter X, Y, D1, D2 of rhombus: ').split()
    x, y, d1, d2 = float(x), float(y), float(d1), float(d2)
    fig_rhombus = Rhombus(x, y, d1, d2)
    print(fig_rhombus)

    rhombus = plt.Polygon(fig_rhombus.coordinates, color='green')
    _, ax = plt.subplots()
    ax.add_artist(rhombus)
    ax.set_xlim((x - d1, x + d1))
    ax.set_ylim((y - d2, y + d2))
    ax.set_aspect('equal')
    plt.title('Rhombus')
    plt.show()

    x, y, r = input('Enter X, Y, R of circumference: ').split()
    x, y, r = float(x), float(y), float(r)
    a, b = input('Enter X, Y of inscribed triangle (should be on circle): ').split()
    a, b = float(a), float(b)
    fig_triangle = InscribedRegularTriangle(x, y, r, Point(a, b))
    print(fig_triangle)

    circle = plt.Circle(fig_triangle.center, fig_triangle.raduis, color='red')
    triangle = plt.Polygon([v.coordinates for v in fig_triangle.vertices], color='blue')
    _, ax = plt.subplots()
    ax.add_artist(circle)
    ax.add_artist(triangle)
    ax.set_xlim((x - 2 * r, x + 2 * r))
    ax.set_ylim((y - 2 * r, y + 2 * r))
    ax.set_aspect('equal')
    plt.show()
