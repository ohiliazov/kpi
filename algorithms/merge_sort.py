def merge_sort(array):
    length = len(array)

    if length == 1:
        return array

    middle = length // 2

    left_part = merge_sort(array[:middle])
    right_part = merge_sort(array[middle:])

    merged_array = merge(left_part, right_part)

    return merged_array


def merge(left_part, right_part):
    left_index = right_index = 0

    merged = []

    while left_index < len(left_part) and right_index < len(right_part):

        if left_part[left_index] > right_part[right_index]:
            merged.append(right_part[right_index])
            right_index += 1
        else:
            merged.append(left_part[left_index])
            left_index += 1

    if left_index < len(left_part):
        merged.extend(left_part[left_index:])
    else:
        merged.extend(right_part[right_index:])

    return merged


def test_merge_sort():
    assert merge_sort([1, 2, 3, 4, 5, 6, 7, 8]) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert merge_sort([8, 7, 6, 5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert merge_sort([3, 7, 4, 8, 1, 5, 2, 6]) == [1, 2, 3, 4, 5, 6, 7, 8]
