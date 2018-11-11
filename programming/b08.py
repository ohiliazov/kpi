"""
Дано натуральні числа a, b, c. Обчислити добуток a, b, c, використовуючи в програмі лише операції +, -, =, <>.
"""


def product(x, y, z):
    xy = 0

    for i in range(y):
        xy += x

    xyz = 0
    for i in range(z):
        xyz += xy

    return xyz


if __name__ == '__main__':
    while True:
        s = input("Enter an array of integers: ")

        if s in ["", "quit", "exit", "close"]:
            break

        try:
            a, b, c = [int(el) for el in s.split()]
            abc = product(a, b, c)
            print(f"Product: {abc}\n")
        except ValueError:
            print("Invalid input. Please use example: 41 12 3\n")
