class SortBase:
    def __init__(self):
        self.array = None

    @property
    def array_size(self):
        return len(self.array)

    def copy_array(self, array):
        self.array = array.copy()

    def swap_items(self, i, j):
        self.array[i], self.array[j] = self.array[j], self.array[i]


class HeapSort(SortBase):
    def __init__(self):
        super().__init__()
        self._heap_size = None

    def _max_heapify(self, i):
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i

        if left < self._heap_size and self.array[left] > self.array[largest]:
            largest = left

        if right < self._heap_size and self.array[right] > self.array[largest]:
            largest = right

        if largest != i:
            self.swap_items(i, largest)
            self._max_heapify(largest)

    def _build_max_heap(self):
        for i in range((self._heap_size // 2), -1, -1):
            self._max_heapify(i)

    def heap_sort(self, array):
        self.copy_array(array)
        self._heap_size = self.array_size
        self._build_max_heap()

        for i in range((self._heap_size - 1), 0, -1):
            self.swap_items(0, i)
            self._heap_size -= 1
            self._max_heapify(0)

        return self.array


class BubbleSort(SortBase):
    def bubble_sort(self, array):
        self.copy_array(array)

        for i in range(self.array_size - 1):
            for j in range(1, self.array_size - i):

                if self.array[j - 1] > self.array[j]:
                    self.swap_items(j - 1, j)

        return self.array

    def bubble_sort_modified(self, array):
        self.copy_array(array)

        swap_index = self.array_size
        for i in range(self.array_size - 1):

            is_sorted = True
            for j in range(1, swap_index):

                if self.array[j - 1] > self.array[j]:
                    self.swap_items(j - 1, j)

                    is_sorted = False
                    swap_index = j

            if is_sorted:
                break

        return self.array


class InsertionSort(SortBase):
    def insertion_sort(self, array):
        self.copy_array(array)

        for i in range(self.array_size):
            for j in range(i, 0, -1):

                if self.array[j - 1] > self.array[j]:
                    self.swap_items(j - 1, j)

        return self.array


class MergeSort(SortBase):
    @staticmethod
    def _merge(left_part, right_part):
        print(left_part,right_part)
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

    def _merge_sort(self, left, right):
        print(self.array[left:right])
        if right - left < 2:
            return [self.array[left]]

        midpoint = (right - left) // 2

        return self._merge(self._merge_sort(left, midpoint),
                           self._merge_sort(midpoint, right))

    def merge_sort(self, array):
        self.copy_array(array)
        self._merge_sort(0, self.array_size - 1)
        return self.array


class SuperSort(HeapSort, BubbleSort, InsertionSort, MergeSort):
    pass


s = SuperSort()
A = [14, 10, 12, 32, 1, 2, 43, 1, 23, 53, 1]
print(A)
print(s.heap_sort(A))
print(A)
print(s.bubble_sort(A))
print(A)
print(s.bubble_sort_modified(A))
print(A)
print(s.insertion_sort(A))
print(A)
print(s.merge_sort(A))
print(A)
