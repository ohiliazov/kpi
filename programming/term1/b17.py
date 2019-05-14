"""
17. Дано  послідовність  із  n  цілих  чисел.
Написати  програму, яка обчислює добуток максимального та мінімального елементів цієї послідовності.
"""


def min_max_product(array):
    x = y = array[0]
    for item in array:
        if item < x:
            x = item
        elif item > y:
            y = item

    return x * y


if __name__ == '__main__':
    print(__doc__)
    while True:
        s = input("Введіть щось: ")

        if s in ["", "quit", "exit", "close"]:
            break

        try:
            input_array = [int(n) for n in s.split()]
            print("Добуток мінімального і максимального члену даної послідновості:", min_max_product(input_array))
        except ValueError:
            print("Невірні дані.")
