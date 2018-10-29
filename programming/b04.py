"""
Для послідовності цілих чисел x[1], … , x[n].
Знайти максимальну довжину її зростаючої підпослідовності (число дій порядку nlog(n)).
"""


def find_largest_sequence(x):
    max_sequence = last_sequence = 1

    for i in range(len(x) - 1):
        if x[i] < x[i+1]:
            last_sequence += 1

            if max_sequence < last_sequence:
                max_sequence = last_sequence

        else:
            last_sequence = 1

    return max_sequence


if __name__ == '__main__':
    while True:
        s = input("Enter an array of integers: ")

        if s in ["", "quit", "exit", "close"]:
            break

        try:
            x = [int(el) for el in s.split()]
        except ValueError:
            print("Invalid input. Please use example: 13 21 1 12\n")

        print(f"Largest sequence length: {find_largest_sequence(x)}\n")
