def bubble_sort(array):
    """ Bubble sort """
    for i in range(len(array) - 1):

        for j in range(len(array) - i - 1):

            if array[j] > array[j + 1]:
                array[j + 1], array[j] = array[j], array[j + 1]

    return array


def bubble_sort_swap_flag(array):
    """ Bubble sort with swap flag """
    for i in range(len(array) - 1):

        is_sorted = True
        for j in range(len(array) - i - 1):

            if array[j] > array[j + 1]:
                array[j + 1], array[j] = array[j], array[j + 1]
                is_sorted = False

        if is_sorted:
            break

    return array


def bubble_sort_swap_index(array):
    """ Bubble sort with swap index """
    length = last_swap_index = len(array)
    for i in range(length - 1):

        for j in range(last_swap_index - 1):

            if array[j] > array[j + 1]:
                array[j + 1], array[j] = array[j], array[j + 1]

                last_swap_index = j

    return array


def bubble_sort_swap_flag_index(array):
    """ Bubble sort with swap flag and index """
    length = last_swap_index = len(array)

    for i in range(length - 1):

        is_sorted = True
        for j in range(1, last_swap_index):

            if array[j - 1] > array[j]:
                array[j - 1], array[j] = array[j], array[j - 1]

                is_sorted = False
                last_swap_index = j

        if is_sorted:
            break

    return array
