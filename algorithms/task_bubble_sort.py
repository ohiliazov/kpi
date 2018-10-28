import random

BUBBLE_COMPARISONS = BUBBLE_ASSIGNMENTS = 0


def bubble_sort_swap_flag(array):
    global BUBBLE_COMPARISONS, BUBBLE_ASSIGNMENTS

    length = last_swap_index = len(array)

    for i in range(length - 1):

        is_sorted = True

        for j in range(1, last_swap_index):

            BUBBLE_COMPARISONS += 1
            if array[j - 1] > array[j]:
                array[j - 1], array[j] = array[j], array[j - 1]

                is_sorted = False
                last_swap_index = j

                BUBBLE_ASSIGNMENTS += 2

        if is_sorted:
            break

    return array


def test_bubble_sort():
    global BUBBLE_COMPARISONS, BUBBLE_ASSIGNMENTS

    for length in [1000, 10000, 100000]:
        BUBBLE_COMPARISONS = BUBBLE_ASSIGNMENTS = 0
        test_array_sorted = [i for i in range(length)]
        bubble_sort_swap_flag(test_array_sorted)

        print("Comparisons for sorted array with %d elements: %.2f" % (length, BUBBLE_COMPARISONS))
        print("Assignments for sorted array with %d elements: %.2f" % (length, BUBBLE_ASSIGNMENTS))

        BUBBLE_COMPARISONS = BUBBLE_ASSIGNMENTS = 0
        test_array_reversed = [i for i in range(length, 0, -1)]
        bubble_sort_swap_flag(test_array_reversed)

        print("Comparisons for reversed array with %d elements: %.2f" % (length, BUBBLE_COMPARISONS))
        print("Assignments for reversed array with %d elements: %.2f" % (length, BUBBLE_ASSIGNMENTS))

        BUBBLE_COMPARISONS = BUBBLE_ASSIGNMENTS = 0
        for i in range(10):
            test_array_random = [random.randrange(1000) for _ in range(length)]
            bubble_sort_swap_flag(test_array_random)

        BUBBLE_COMPARISONS /= 10
        BUBBLE_ASSIGNMENTS /= 10

        print("Comparisons for random array with %d elements: %.2f" % (length, BUBBLE_COMPARISONS))
        print("Assignments for random array with %d elements: %.2f\n" % (length, BUBBLE_ASSIGNMENTS))


test_bubble_sort()
