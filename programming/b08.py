"""
Дано натуральні числа a, b, c. Обчислити добуток a, b, c, використовуючи в програмі лише операції +, -, =, <>.
"""


def find_product(a, b, c):
    a_b = 0

    for i in range(b):
        a_b += a

    a_b_c = 0
    for i in range(c):
        a_b_c += a_b

    return a_b_c


if __name__ == '__main__':
    while True:
        s = input("Enter an array of integers: ")

        if s in ["", "quit", "exit", "close"]:
            break

        try:
            a, b, c = [int(el) for el in s.split()]
        except ValueError:
            print("Invalid input. Please use example: 41 12 3\n")
            continue

        print(f"Product: {find_product(a, b, c)}\n")
