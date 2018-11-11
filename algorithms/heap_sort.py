def max_heapify(array, heap_size, i):
    left = 2 * i + 1
    right = 2 * i + 2
    largest = i

    if left < heap_size and array[left] > array[largest]:
        largest = left

    if right < heap_size and array[right] > array[largest]:
        largest = right

    if largest != i:
        array[i], array[largest] = array[largest], array[i]
        max_heapify(array, heap_size, largest)


def build_max_heap(array):
    heap_size = len(array)

    for i in range((heap_size // 2), -1, -1):
        max_heapify(array, heap_size, i)


def heap_sort(array):
    heap_size = len(array)
    build_max_heap(array)

    for i in range(heap_size - 1, 0, -1):
        array[0], array[i] = array[i], array[0]
        heap_size -= 1
        max_heapify(array, heap_size, 0)


