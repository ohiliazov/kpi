import os
from collections import UserList
from functools import total_ordering


@total_ordering
class Date:
    def __init__(self, year: int, month: int, day: int):
        if not all(isinstance(item, int) for item in (year, month, day)):
            raise TypeError("Year, month and day should be integers")

        is_leap = (year % 4) == 0 and (year % 100) != 0 or (year % 100) == 0 and (year % 400) == 0

        if month < 1 or month > 12:
            raise ValueError("Month is out of bounds")

        if (day < 1
                or month == 2 and day > 28 + is_leap    # Feb
                or month in [4, 6, 9, 11] and day > 30  # Apr Jun Sep Nov
                or day > 31):                           # Jan Mar May Jul Aug Oct Dec
            raise ValueError("Day is out of bounds")

        self.year = year
        self.month = month
        self.day = day

    def __str__(self):
        return f"{self.day:02d}-{self.month:02d}-{self.year%100:02d}"

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


class DateCollection(UserList):
    def append(self, item: Date) -> None:
        if not isinstance(item, Date):
            raise TypeError('Only ``Date`` is allowed')
        super().append(item)

    def insert(self, i: int, item: Date) -> None:
        if not isinstance(item, Date):
            raise TypeError('Only ``Date`` is allowed')
        super().insert(i, item)

    def swap(self, k, j):
        if k >= len(self) or j >= len(self):
            raise IndexError('Out of bounds')
        self[k], self[j] = self[j], self[k]

    def display(self):
        print('########')
        for item in self:
            print(item)
        print('########')

    def sort_by_year(self):
        self.sort(key=lambda item: item.year)

    def sort_by_month(self):
        self.sort(key=lambda item: item.month)

    def sort_by_day(self):
        self.sort(key=lambda item: item.day)

    def remove_recent_items(self, threshold: Date):
        new_list = []
        for item in self:
            if item <= threshold:
                new_list.append(item)

        return new_list

    def save_winter_dates_to_file(self):
        with open(os.path.join(os.getcwd(), 'winter_dates.txt'), 'w+') as f:
            for item in self:
                if item.month in [12, 1, 2]:
                    f.write(str(item) + '\n')


if __name__ == '__main__':
    dates = DateCollection()
    length = int(input("Enter array size: "))

    for _ in range(length):
        d = input("Enter date in format YYYY-MM-DD: ")
        year, month, day = d.split('-')
        dates.append(Date(int(year), int(month), int(day)))

    print('Initial array')
    dates.display()

    print('Sort by year')
    dates.sort_by_year()

    print('Swap first with last')
    dates.swap(0, -1)
    dates.display()

    d = input('Enter date threshold in format YYYY-MM-DD:')
    year, month, day = d.split('-')
    dates.remove_recent_items(Date(int(year), int(month), int(day)))
    dates.display()

    print('Save winter dates into file winter_dates.txt')
    dates.save_winter_dates_to_file()
