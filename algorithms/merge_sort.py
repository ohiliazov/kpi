import random, sys


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


merge_sort(random.sample(range(sys.maxsize), 1000000))