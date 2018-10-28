import datetime
import random

RADIX_ASSIGNMENTS = 0


def stable_sort(array, pos):
    global RADIX_ASSIGNMENTS

    def get_digit(item, pos):
        global RADIX_ASSIGNMENTS
        for _ in range(pos):
            item //= 10
        return item % 10

    buckets = [[], [], [], [], [], [], [], [], [], []]

    for item in array:
        RADIX_ASSIGNMENTS += 1
        buckets[get_digit(item, pos)].append(item)

    array = []

    for bucket in buckets:
        array.extend(bucket)

    return array


def radix_sort(array):
    max_value = max(array)

    max_digits = 0
    while max_value > 0:
        max_value //= 10
        max_digits += 1

    for pos in range(max_digits):
        array = stable_sort(array, pos)

    return array


def test_radix_sort():
    global RADIX_ASSIGNMENTS
    time_start = datetime.datetime.now()

    for length in [1000, 10000, 100000]:
        RADIX_ASSIGNMENTS = 0
        test_array_sorted = [i for i in range(length)]
        radix_sort(test_array_sorted)

        print("Assignments for sorted array with %d elements: %.2f" % (length, RADIX_ASSIGNMENTS))

        RADIX_ASSIGNMENTS = 0
        test_array_reversed = [i for i in range(length-1, -1, -1)]
        radix_sort(test_array_reversed)

        print("Assignments for reversed array with %d elements: %.2f" % (length, RADIX_ASSIGNMENTS))

        RADIX_ASSIGNMENTS = 0
        for i in range(1000):
            test_array_random = [random.randrange(length-1) for _ in range(length)]
            radix_sort(test_array_random)

        RADIX_ASSIGNMENTS /= 1000

        print("Assignments for random array with %d elements: %.2f\n" % (length, RADIX_ASSIGNMENTS))

    time_stop = datetime.datetime.now()

    print(datetime.timedelta.total_seconds(time_stop - time_start))


test_radix_sort()
