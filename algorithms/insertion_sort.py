def insertion_sort(array):
    length = len(array)

    for i in range(length):
        for j in range(i, 0, -1):

            if array[j - 1] > array[j]:
                array[j - 1], array[j] = array[j], array[j - 1]

    return array
