import math
from functools import total_ordering


@total_ordering
class Date:
    def __init__(self, year: int, month: int, day: int):
        self.set_year(year)
        self.set_month(month)
        self.set_day(day)

        self.month_table = {
            1: 31,
            2: 28 + self.is_leap,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31,
        }

    def __str__(self):
        return f"{self.year}-{self.month}-{self.day}"

    def __repr__(self):
        return f"Date{(self.year, self.month, self.day)}"

    def __eq__(self, other):
        return self.year == other.year and self.month == other.month and self.day == other.day

    def __lt__(self, other):
        if self.year != other.year:
            return self.year < other.year

        if self.month != other.month:
            return self.month < other.month

        return self.day < other.day

    def __add__(self, other: int):
        new_date = self.copy()
        sum_days = new_date.day + other
        while sum_days > new_date.month_table[new_date.month]:
            sum_days -= new_date.month_table[new_date.month]

            try:
                new_date.set_month(new_date.month + 1)
            except ValueError:
                new_date.set_year(new_date.year + 1)
                new_date.set_month(1)

        new_date.set_day(sum_days)

        return new_date

    def __iadd__(self, other: int):
        sum_days = self.day + other
        while sum_days > self.month_table[self.month]:
            sum_days -= self.month_table[self.month]

            try:
                self.set_month(self.month + 1)
            except ValueError:
                self.set_year(self.year + 1)
                self.set_month(1)

        self.set_day(sum_days)

        return self

    @classmethod
    def from_string(cls, date_string: str):
        year, month, day = date_string.split('-')
        return Date(int(year), int(month), int(day))

    @property
    def is_leap(self):
        return (self.year % 4) == 0 and (self.year % 100) != 0 \
               or (self.year % 100) == 0 and (self.year % 400) == 0

    def get_year(self):
        return self.year

    def get_month(self):
        return self.month

    def get_day(self):
        return self.day

    def set_year(self, year):
        if not isinstance(year, int):
            raise TypeError("Year should be integer")
        self.year = year

        return self

    def set_month(self, month):
        if not isinstance(month, int):
            raise TypeError("Month should be integer")

        if month < 1 or month > 12:
            raise ValueError("Month is out of bounds")

        self.month = month

        return self

    def set_day(self, day):
        if not isinstance(day, int):
            raise TypeError("Day should be integer")

        if (day < 1
                or self.month == 2 and day > 28 + self.is_leap  # Feb
                or self.month in [4, 6, 9, 11] and day > 30  # Apr Jun Sep Nov
                or day > 31):  # Jan Mar May Jul Aug Oct Dec
            raise ValueError("Day is out of bounds")

        self.day = day

        return self

    def copy(self):
        return Date(self.year, self.month, self.day)


class Point:
    def __init__(self, x: [int, float], y: [int, float]):
        self.set_x(x)
        self.set_y(y)

    def __str__(self):
        return f"Point({round(self.x, 2)}, {round(self.y, 2)})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @classmethod
    def from_string(cls, xy_string: str):
        x, y = xy_string.split(',')
        return Point(float(x), float(y))

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


class Circle:
    def __init__(self, x: [int, float], y: [int, float], r: [int, float]):
        self.center = Point(x, y)
        self.set_radius(r)

    def __str__(self):
        return f"Circle(center={str(self.center.coordinates)}, radius={round(self.radius, 2)})"

    def __eq__(self, other):
        return self.center == other.center and self.radius == other.radius

    def __lt__(self, other: 'Circle'):
        return self.radius < other.radius

    def set_radius(self, r):
        if not isinstance(r, (int, float)):
            raise TypeError('Radius should be a number')
        self.radius = r
