class Date:
    def __init__(self, year: int, month: int, day: int):
        self.year = None
        self.month = None
        self.day = None
        self.set_year(year)
        self.set_month(month)
        self.set_day(day)

    def as_string(self):
        return f"{self.year} {self.month} {self.day}"

    def as_repr(self):
        return f"Date{(self.year, self.month, self.day)}"

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
                or self.month in [4, 6, 9, 11] and day > 30     # Apr Jun Sep Nov
                or day > 31):                                   # Jan Mar May Jul Aug Oct Dec
            raise ValueError("Day is out of bounds")

        self.day = day

        return self

    def copy(self):
        return Date(self.year, self.month, self.day)


class Dot:
    def __init__(self, i: int, x: [int, float], y: [int, float]):
        self.i = i
        self.x = None
        self.y = None

        self.set_x(x)
        self.set_y(y)

    def as_string(self):
        return f"{self.x} {self.y}"

    def as_repr(self):
        return f"Dot{(self.x, self.y)}"

    def set_x(self, x):
        if not isinstance(x, (int, float)):
            raise TypeError('Coordinated should be a number')
        self.x = x

        return self

    def set_y(self, y):
        if not isinstance(y, (int, float)):
            raise TypeError('Coordinated should be a number')
        self.y = y

        return self


if __name__ == '__main__':
    date_one = Date(2019, 5, 14)
    date_two = Date.from_string('2019-05-15')
    date_three = Date(2012, 12, 20)

    for d in [date_one, date_two, date_three]:
        print(d.as_string())
        print(d.as_repr())

    dot_one = Dot(0, 1, 1)
    dot_two = Dot(1, 1, 2.5)
    dot_three = Dot(1, 2.5, 7.0)

    for d in [dot_one, dot_two, dot_three]:
        print(d.as_string())
        print(d.as_repr())
