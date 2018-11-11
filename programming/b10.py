"""
10. Дано натуральне n.
Підрахувати кількість розв’язків нерівності x^2+y^2<n в натуральних (невід’ємних числах)
не використовуючи дій з дійсними числами. Кількість операцій повинна бути порядку √n.
"""

import math


def count_int_roots(n):
    r = math.ceil(math.sqrt(n))

    counter = 0
    for x in range(r):
        y = math.sqrt(n - x * x)
        counter += math.ceil(y)

    return counter


if __name__ == '__main__':
    print(__doc__)
    while True:
        input_n = input("Введіть число: ")

        if input_n in ["", "quit", "exit", "close"]:
            break

        try:
            print("Кількість розв'язків:", count_int_roots(float(input_n)))
        except ValueError:
            print("Невірні дані.")
