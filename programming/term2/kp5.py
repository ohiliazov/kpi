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
        return (self.x, self.y),

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

    def get_circle(self, radius):
        return Circle(self.x, self.y, radius)

    def get_rhombus(self, d1, d2):
        return Rhombus(self.x, self.y, d1, d2)


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

    def get_figures(self):
        return [plt.Polygon(self.coordinates, color='green')]

    def get_point(self):
        return Point(self.x, self.y)


class Circle(Point):
    def __init__(self, x: [int, float], y: [int, float], r: [int, float]):
        super().__init__(x, y)
        self.set_radius(r)

    def __str__(self):
        return f"Circle(center={str(self.center)}, radius={round(self.raduis, 2)})"

    @property
    def coordinates(self):
        return (self.x + self.raduis, self.y + self.raduis), (self.x - self.raduis, self.y - self.raduis)

    @property
    def center(self):
        return self.x, self.y

    def set_radius(self, r):
        if not isinstance(r, (int, float)):
            raise TypeError('Radius should be a number')
        self.raduis = r

    def get_figures(self):
        return [plt.Circle(self.center, self.raduis, color='red')]

    def get_point(self):
        return Point(self.x, self.y)


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

    def get_figures(self):
        circle = plt.Circle(self.center, self.raduis, color='red')
        triangle = plt.Polygon([v.coordinates for v in self.vertices], color='blue')

        return [circle, triangle]


class Image:
    def __init__(self, *args):
        self.items = []

        for item in args:
            self.add_item(item)

    def add_item(self, item):
        self.items.append(item)

    @property
    def count(self):
        return len(self.items)

    def get_all_figures(self):
        figures = []
        try:
            for item in self.items:
                if isinstance(item, (Circle, Rhombus, InscribedRegularTriangle)):
                    figures.extend(item.get_figures())
        except:
            pass

        return figures

    def plot(self):
        fig, ax = plt.subplots()

        min_x, max_x, min_y, max_y = 0, 0, 0, 0
        for item in self.items:
            for coord in item.coordinates:
                min_x = min(min_x, coord[0])
                min_y = min(min_y, coord[1])
                max_x = max(max_x, coord[0])
                max_y = max(max_y, coord[1])

        for figure in self.get_all_figures():
            ax.add_artist(figure)

        ax.set_xlim((min_x, max_x))
        ax.set_ylim((min_y, max_y))
        ax.set_aspect('equal')
        plt.show()


if __name__ == '__main__':
    p = Point(-1, -2)
    c = p.get_circle(2)
    r = Rhombus(1, 2, 3, 4)
    i = InscribedRegularTriangle(2, 2, 1, Point(3, 2))
    img = Image(c, r, i)
    img.plot()
