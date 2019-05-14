"""
Написати програму, яка на основі алгоритму сортування злиттям одномірного масиву знаходить
число інверсій в одновимірному масиві ai=100sin(i*N) розмірності 500000.
"""
from math import sin


class InverseCounter:
    def __init__(self):
        self.inverse_count = 0

    def count_inverses(self, array):
        self.inverse_count = 0
        self.merge_sort(array)

        return self.inverse_count

    def merge_sort(self, array):
        if len(array) == 1:
            return array

        mid_point = len(array) // 2
        left, right = array[:mid_point], array[mid_point:]

        return self.merge(self.merge_sort(left), self.merge_sort(right))

    def merge(self, left, right):
        left_index = right_index = 0
        merged = []

        for i in range(len(left) + len(right)):
            if left_index < len(left) and right_index < len(right):

                if left[left_index] > right[right_index]:
                    merged.append(right[right_index])
                    self.inverse_count += len(left) - left_index
                    right_index += 1
                else:
                    merged.append(left[left_index])
                    left_index += 1

            else:
                if left_index < len(left):
                    merged.append(left[left_index])
                    left_index += 1
                else:
                    merged.append(right[right_index])
                    right_index += 1

        return merged


if __name__ == '__main__':
    counter = InverseCounter()

    while True:
        s = input("Enter a float number: ")

        if s in ["", "quit", "exit", "close"]:
            break

        try:
            n = float(s)
        except ValueError:
            print("Invalid input.\n")
            continue

        a = [100 * sin(i * n) for i in range(500000)]
        print(f"Inverse count: {counter.count_inverses(a)}\n")
