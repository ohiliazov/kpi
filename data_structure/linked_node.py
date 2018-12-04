"""
2-11. Створити однозв’язний список дисциплін факультету, кожний елемент якого містить загальну інформацію по дисципліні
(назва, кількість кредитів) та деталізовану інформацію про номер семестру, у якому дисципліна викладається, кількість
аудиторних годин, кількість лекційних годин, кількість МКР та ознаку семестрового контролю (залік/екзамен)).

    1) Реалізувати функції перегляду записаних даних, додавання нового елемента на задану позицію (INSERT), видалення
    елемента з заданої позиції (DELETE). Початковий вміст списку заповнити з клавіатури.

    2) Впорядкувати записи за номером семестру, а в межах одного семестру — за кількістю аудиторних годин у порядку
    спадання.
"""


class NodeNotFound(Exception):
    pass


class LinkedNode:
    def __init__(self, key, data, next_node=None):
        self.key = key
        self.data = data
        self.next = next_node

    def __str__(self):
        return f"{self.key} {self.data['name']:50s} {self.data['term']:1d} сем. {self.data['class_hours']:3d} год."


class LinkedList:
    def __init__(self, head=None):
        self.head = head

    def __str__(self):
        result = str(self.head)
        node = self.head
        while node.next:
            node = node.next
            result += "\n" + str(node)

        return result

    def find(self, key):
        print(f"Looking for node with key {key}")
        node = self.head

        if not node:
            raise NodeNotFound(f"Node with key {key} not found")

        if key == node.key:
            return node

        while node.next:
            node = node.next
            if key == node.key:
                return node

    def add_to_head(self, node):
        print(f"Adding node {node.key} to head")
        node.next = self.head
        self.head = node

    def add_to_end(self, node):
        print(f"Adding node {node.key} to end")
        if not self.head:
            self.head = node
            return

        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = node

    def insert_after_node(self, parent_key, node):
        parent = self.find(parent_key)

        print(f"Adding node {node.key} after node {parent_key}")
        node.next = parent.next
        parent.next = node

    def delete(self, key):
        print(f"Removing node {key}")
        node = self.head

        if not node:
            return

        if node.key == key:
            self.head = node.next
            del node
            return

        while node.next:
            if node.next.key == key:
                node.next = node.next.next
                return
            node = node.next

    def merge(self, left, right, key='name'):
        if not left:
            return right
        if not right:
            return left

        if left.data[key] <= right.data[key]:
            result = left
            result.next = self.merge(left.next, right, key)

        else:
            result = right
            result.next = self.merge(left, right.next)

        return result

    def merge_sort(self, head=None, key='name'):
        head = head or self.head
        if not head or not head.next:
            return head

        middle_node = self.get_middle_node(head)
        middle_next_node = middle_node.next
        middle_node.next = None

        left = self.merge_sort(head, key)
        right = self.merge_sort(middle_next_node, key)

        self.head = self.merge(left, right, key)

        return self.head

    def get_middle_node(self, head):
        head = head or self.head
        if not head:
            return

        slow_pointer = head
        fast_pointer = head.next

        while fast_pointer:
            fast_pointer = fast_pointer.next

            if fast_pointer:
                slow_pointer = slow_pointer.next
                fast_pointer = fast_pointer.next

        return slow_pointer


def parse_input(prompt, data_type):
    while True:
        try:
            return data_type(input(prompt))
        except ValueError:
            print("Невірне значення. Спробуйте зе раз.")


def input_node_data():
    print()
    data = {'name': parse_input("Введіть назву дисципліни: ", str),
            'credit': parse_input("Введіть кількість кредитів: ", int),
            'term': parse_input("Введіть номер семестру: ", int),
            'class_hours': parse_input("Введіть кількість аудіторних годин: ", int),
            'lecture_hours': parse_input("Введіть кількість лекційних годин: ", int),
            'work': parse_input("Введіть кількість МКР: ", int),
            'exam': parse_input("Введіть ознаку семетрового контролю (0 - залік/1 - екзамен): ", bool)}

    return data


def test_linked_node():
    subjects = [
        {'name': "Аглебра і геометрія",
         'credit': 56, 'term': 5, 'class_hours': 30,
         'lecture_hours': 40, 'work': 9, 'exam': False},
        {'name': "Математичний аналіз",
         'credit': 60, 'term': 5, 'class_hours': 45,
         'lecture_hours': 45, 'work': 34, 'exam': False},
        {'name': "Дискретна математика",
         'credit': 99, 'term': 4, 'class_hours': 60,
         'lecture_hours': 20, 'work': 6, 'exam': True},
        {'name': "Програмування",
         'credit': 100, 'term': 6, 'class_hours': 60,
         'lecture_hours': 25, 'work': 3, 'exam': True},
        {'name': "Алгоритми і структури даних",
         'credit': 80, 'term': 5, 'class_hours': 50,
         'lecture_hours': 20, 'work': 3, 'exam': True},
        {'name': "Проектування та аналіз обчислювальних алгоритмів",
         'credit': 76, 'term': 7, 'class_hours': 30,
         'lecture_hours': 70, 'work': 5, 'exam': True},
        {'name': "Операційні системи",
         'credit': 54, 'term': 3, 'class_hours': 36,
         'lecture_hours': 29, 'work': 5, 'exam': False},
    ]
    n1 = LinkedNode(1, subjects[0])
    n2 = LinkedNode(2, subjects[1])
    n3 = LinkedNode(3, subjects[2])
    n4 = LinkedNode(4, subjects[3])
    n5 = LinkedNode(5, subjects[4])
    n6 = LinkedNode(6, subjects[5])
    n7 = LinkedNode(7, subjects[6])
    root = LinkedList()

    print("\n\nADD TWO ELEMENTS TO HEAD")
    root.add_to_head(n1)
    root.add_to_head(n2)
    print()
    print(root)

    print("\n\nADD TWO ELEMENTS TO END")
    root.add_to_end(n3)
    root.add_to_end(n4)
    print()
    print(root)

    print("\n\nADD TWO ELEMENTS BETWEEN")
    root.insert_after_node(1, n5)
    root.insert_after_node(3, n6)
    print()
    print(root)

    print("\n\nDELETE ELEMENT AT HEAD")
    root.delete(2)
    print()
    print(root)

    print("\n\nDELETE ELEMENT AT END")
    root.delete(4)
    print()
    print(root)

    print("\n\nADD ELEMENTS")
    root.add_to_head(n2)
    root.add_to_end(n4)
    print()
    print(root)

    print("\n\nMERGE SORT BY CLASS HOURS AND TERM")
    root.merge_sort(key='class_hours')
    root.merge_sort(key='term')
    print()
    print(root)


if __name__ == '__main__':
    test_linked_node()
    print("\nTEST FINISHED\n\n")
    n = parse_input("Введіть кілкість дисциплін: ", int)

    root = LinkedList()
    node_key = 1
    for i in range(n):
        input_data = input_node_data()
        node = LinkedNode(node_key, input_data)
        root.add_to_head(node)
        node_key += 1

    print(root)
    root.merge_sort(key='class_hours')
    root.merge_sort(key='term')
    print()
    print(root)
