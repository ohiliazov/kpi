def bubble_sort(array):
    length = len(array)
    for i in range(length - 1):

        for j in range(length - i - 1):

            if array[j] > array[j + 1]:
                array[j + 1], array[j] = array[j], array[j + 1]

    return array


def bubble_sort_flag(array):
    length = len(array)

    for i in range(length - 1):

        is_sorted = True

        for j in range(length - i - 1):

            if array[j] > array[j + 1]:
                array[j + 1], array[j] = array[j], array[j + 1]
                is_sorted = False

        if is_sorted:
            break

    return array


def test_bubble_sort():
    assert bubble_sort([1, 2, 3, 4, 5, 6, 7, 8]) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert bubble_sort([8, 7, 6, 5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert bubble_sort([3, 7, 4, 8, 1, 5, 2, 6]) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert bubble_sort_flag([1, 2, 3, 4, 5, 6, 7, 8]) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert bubble_sort_flag([8, 7, 6, 5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert bubble_sort_flag([3, 7, 4, 8, 1, 5, 2, 6]) == [1, 2, 3, 4, 5, 6, 7, 8]
