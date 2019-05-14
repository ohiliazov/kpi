"""
Для послідовності цілих чисел x[1], … , x[n].
Знайти максимальну довжину її зростаючої підпослідовності (число дій порядку nlog(n)).
"""


def max_seq_length(x):
    max_len = length = 1

    for i in range(len(x) - 1):
        if x[i] < x[i + 1]:
            length += 1

            if max_len < length:
                max_len = length

        else:
            length = 1

    return max_len


if __name__ == '__main__':
    while True:
        s = input("Enter an array of integers: ")

        if s in ["", "quit", "exit", "close"]:
            break

        try:
            x = [int(el) for el in s.split()]
            max_seq_x = max_seq_length(x)
            print(f"Largest sequence length: {max_seq_x}\n")
        except ValueError:
            print("Invalid input. Please use example: 13 21 1 12\n")
