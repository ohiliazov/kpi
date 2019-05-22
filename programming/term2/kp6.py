from functools import partial


class Object:
    def __init__(self, i):
        self.i = i

    def __eq__(self, other):
        return self.i == other.i

    def __str__(self):
        return f"Object({self.i})"

    def __repr__(self):
        return f"Object({self.i})"


list1 = [1, 2, 3, 4, 5, 6, 1, 2, 3]
list2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'b', 'c', 'd', 'f', 'g', 'b']
list3 = [0.5, 1.6, 2.7, 3.8, 4.9, 5.0, 6.1, 7.2, 8.3, 6.1, 7.2, 8.3]
list4 = [Object(1), Object('a'), Object(5.6), Object('b')]

value1 = 3
value2 = 'b'
value3 = 0.5
value4 = Object('a')


def indices(array: list, value, value_type: type) -> list:
    if not isinstance(value, value_type):
        print(f'Value {value} is not {value_type.__name__}, but {type(value).__name__}')
        raise TypeError

    idxs = []
    for i in range(len(array)):
        if array[i] == value:
            idxs.append(i)

    return idxs


int_indices = partial(indices, value_type=int)
str_indices = partial(indices, value_type=str)
float_indices = partial(indices, value_type=float)
object_indices = partial(indices, value_type=Object)

if __name__ == '__main__':
    print('Correct types...')
    print(f'Integer function: {value1} in {list1} => {int_indices(list1, value1)}')
    print(f'String function: {value2} in {list2} => {str_indices(list2, value2)}')
    print(f'Float function: {value3} in {list3} => {float_indices(list3, value3)}')
    print(f'Object function: {value4} in {list4} => {object_indices(list4, value4)}')

    print('Wrong types...')
    try:
        print(f'Integer function: {value2} in {list1} => {int_indices(list1, value2)}')
    except TypeError:
        pass

    try:
        print(f'String function: {value3} in {list2} => {str_indices(list2, value3)}')
    except TypeError:
        pass

    try:
        print(f'Float function: {value4} in {list3} => {float_indices(list3, value4)}')
    except TypeError:
        pass

    try:
        print(f'Object function: {value1} in {list4} => {object_indices(list4, value1)}')
    except TypeError:
        pass
