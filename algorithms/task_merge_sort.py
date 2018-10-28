import datetime
import random

MERGE_COMPARISONS = MERGE_ASSIGNMENTS = 0


def merge_sort(array):
    global MERGE_COMPARISONS, MERGE_ASSIGNMENTS

    def merge(left_part, right_part):
        global MERGE_COMPARISONS, MERGE_ASSIGNMENTS
        left_length = len(left_part)
        right_length = len(right_part)

        left_index = right_index = 0

        merged = []

        while left_index < left_length and right_index < right_length:
            MERGE_COMPARISONS += 1
            MERGE_ASSIGNMENTS += 1
            if left_part[left_index] > right_part[right_index]:
                merged.append(right_part[right_index])
                right_index += 1
            else:
                merged.append(left_part[left_index])
                left_index += 1

        if left_index < left_length:
            merged.extend(left_part[left_index:])
            MERGE_ASSIGNMENTS += len(left_part[left_index:])
        else:
            merged.extend(right_part[right_index:])
            MERGE_ASSIGNMENTS += len(right_part[right_index:])

        return merged

    if len(array) == 1:
        return array

    midpoint = len(array) // 2
    return merge(merge_sort(array[:midpoint]), merge_sort(array[midpoint:]))


def test_merge_sort():
    global MERGE_COMPARISONS, MERGE_ASSIGNMENTS
    time_start = datetime.datetime.now()

    for length in [1000, 10000, 100000]:
        MERGE_COMPARISONS = MERGE_ASSIGNMENTS = 0
        test_array_sorted = [i for i in range(length)]
        merge_sort(test_array_sorted)

        print("Comparisons for sorted array with %d elements: %.2f" % (length, MERGE_COMPARISONS))
        print("Assignments for sorted array with %d elements: %.2f" % (length, MERGE_ASSIGNMENTS))

        MERGE_COMPARISONS = MERGE_ASSIGNMENTS = 0
        test_array_reversed = [i for i in range(length, 0, -1)]
        merge_sort(test_array_reversed)

        print("Comparisons for reversed array with %d elements: %.2f" % (length, MERGE_COMPARISONS))
        print("Assignments for reversed array with %d elements: %.2f" % (length, MERGE_ASSIGNMENTS))

        MERGE_COMPARISONS = MERGE_ASSIGNMENTS = 0
        for i in range(1000):
            test_array_random = [random.randrange(1000) for _ in range(length)]
            merge_sort(test_array_random)

        MERGE_COMPARISONS /= 1000
        MERGE_ASSIGNMENTS /= 1000

        print("Comparisons for random array with %d elements: %.2f" % (length, MERGE_COMPARISONS))
        print("Assignments for random array with %d elements: %.2f\n" % (length, MERGE_ASSIGNMENTS))

    time_stop = datetime.datetime.now()

    print(datetime.timedelta.total_seconds(time_stop - time_start))


test_merge_sort()
