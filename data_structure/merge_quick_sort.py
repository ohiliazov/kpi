import os
import random
import sys
import time

DATA_LENGTH = {
    "XS":  1000,
    "S":   10000,
    "M":   100000,
    "L":   1000000,
    "XL":  10000000,
    "XXL": 100000000,
}


def merge(left_part, right_part):
    merged = []

    i = j = 0
    while i < len(left_part) and j < len(right_part):

        if left_part[i] < right_part[j]:
            merged.append(left_part[i])
            i += 1
        else:
            merged.append(right_part[j])
            j += 1

    if i < len(left_part):
        merged.extend(left_part[i:])
    elif j < len(right_part):
        merged.extend(right_part[j:])

    return merged


def merge_sort(array):
    if len(array) == 1:
        return array

    midpoint = len(array) // 2

    return merge(merge_sort(array[:midpoint]),
                 merge_sort(array[midpoint:]))


def quick_sort(array, first, last):
    if first < last:
        split_point = partition(array, first, last)

        quick_sort(array, first, split_point - 1)
        quick_sort(array, split_point + 1, last)

    return array


def partition(array, first, last):
    pivot = array[first]

    left = first + 1
    right = last

    done = False
    while not done:

        while left <= right and array[left] <= pivot:
            left = left + 1

        while array[right] >= pivot and right >= left:
            right = right - 1

        if right < left:
            done = True
        else:
            array[left], array[right] = array[right], array[left]

    array[first], array[right] = array[right], array[first]

    return right


def timer(func):
    def wrapper(*args):
        start = time.clock()
        func(*args)
        end = time.clock()
        print(f"Elapsed time: {end - start:.2f} seconds")

    return wrapper


@timer
def generate_data(size):
    if os.path.exists("data.in"):
        os.remove("data.in")

    with open("data.in", "w+") as fd:
        for number in random.sample(range(sys.maxsize), DATA_LENGTH[size]):
            fd.write(f"{number}\n")


@timer
def merge_sort_data():
    array = []
    with open("data.in", "r") as data:
        line = data.readline()
        while line:
            array.append(int(line))
            line = data.readline()
    merged = merge_sort(array)

    if os.path.exists("data.out"):
        os.remove("data.out")

    with open("data.out", "w+") as output:
        output.writelines([f"{i}\n" for i in merged])


@timer
def quick_sort_data():
    array = []
    with open("data.in", "r") as data:
        line = data.readline()
        while line:
            array.append(int(line))
            line = data.readline()

    merged = quick_sort(array, 0, len(array) - 1)

    if os.path.exists("data.out"):
        os.remove("data.out")

    with open("data.out", "w+") as output:
        output.writelines([f"{i}\n" for i in merged])


def print_data_out_top(lines=5):
    with open("data.out", "r") as fd:
        i = 0
        line = fd.readline()
        while line and i < lines:
            print(line.strip())
            line = fd.readline()
            i += 1


def run_merge_sort(size):
    print(f"\nGenerate data.in (size {size})")
    generate_data(size)
    print(f"Perform merge sort (size {size})")
    merge_sort_data()
    print("Top 5 values:")
    with open("data.out", "r") as fd:
        i = 0
        line = fd.readline()
        while line and i < 5:
            print(line.strip())
            line = fd.readline()
            i += 1


def run_quick_sort(size):
    print(f"\nGenerate data.in (size {size})")
    generate_data(size)
    print(f"Perform quick sort (size {size})")
    quick_sort_data()
    print("Top 5 values:")
    with open("data.out", "r") as fd:
        i = 0
        line = fd.readline()
        while line and i < 5:
            print(line.strip())
            line = fd.readline()
            i += 1


if __name__ == '__main__':
    # MERGE SORT
    run_merge_sort("XS")   # GEN:   0.00  SORT:   0.00
    run_merge_sort("S")    # GEN:   0.01  SORT:   0.04
    run_merge_sort("M")    # GEN:   0.11  SORT:   0.49
    run_merge_sort("L")    # GEN:   1.17  SORT:   5.83
    run_merge_sort("XL")   # GEN:  12.16  SORT:  73.54
    run_merge_sort("XXL")  # GEN: 137.65  SORT: 884.29

    # QUICK SORT
    run_quick_sort("XS")   # GEN:   0.01  SORT:   0.01
    run_quick_sort("S")    # GEN:   0.03  SORT:   0.04
    run_quick_sort("M")    # GEN:   0.11  SORT:   0.31
    run_quick_sort("L")    # GEN:   1.18  SORT:   3.93
    run_quick_sort("XL")   # GEN:  12.00  SORT:  48.27
    run_quick_sort("XXL")  # GEN: 130.70  SORT: 620.42
