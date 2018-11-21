class NodeTreeNotFound(KeyError):
    pass


class NodeTreeDuplicateError(KeyError):
    pass


class NodeTreeRotationError(KeyError):
    pass


class Node:
    def __init__(self, key: int, value: str = None):
        self.key = key
        self.value = value
        self.left = NodeTree()
        self.right = NodeTree()

    def __str__(self):
        return f"{self.key} {self.value}"

    def __repr__(self):
        return f"{self.key}"

    def __lt__(self, other: "Node"):
        return self.key < other.key

    def __gt__(self, other: "Node"):
        return self.key > other.key

    def replace(self, node: "Node"):
        self.key = node.key
        self.value = node.value

    def is_leaf(self):
        return self.left.node is None and self.right.node is None


class NodeTree:
    def __init__(self, *nodes):
        self.node = None  # type: Node

        for node in nodes:
            self._insert(node)

    def __repr__(self):
        return ""

    def display(self, depth=0):
        indent = "    " * depth
        result = f"{indent}{self.node}\n"

        if self.left_node:
            result += self.left_tree.display(depth + 1)

        if self.right_node:
            result += self.right_tree.display(depth + 1)

        return result

    def get_tree(self, key):
        if key == self.node.key:
            return self

        elif key < self.node.key and self.left_node:
            return self.left_tree.get_tree(key)

        elif key > self.node.key and self.right_node:
            return self.right_tree.get_tree(key)

        raise NodeTreeNotFound(f"Node {key} not found in tree.")

    @property
    def left_tree(self):
        if self.node:
            return self.node.left

    @property
    def left_node(self):
        return self.left_tree.node

    @property
    def right_tree(self):
        if self.node:
            return self.node.right

    @property
    def right_node(self):
        return self.right_tree.node

    @property
    def height(self):
        if self.left_node is None and self.right_node is None:
            return 1

        if self.left_node:
            return 1 + self.left_tree.height

        if self.right_node:
            return 1 + self.right_tree.height

        return 1 + max(self.left_tree.height, self.right_tree.height)

    @property
    def balance_factor(self):

        if self.left_node is None and self.right_node is None:
            balance_factor = 0

        elif self.left_node is None:
            balance_factor = self.right_tree.height

        elif self.right_node is None:
            balance_factor = -self.left_tree.height

        else:
            balance_factor = self.right_tree.height - self.left_tree.height

        return balance_factor

    @property
    def is_balanced(self):
        return -2 < self.balance_factor < 2

    def _insert(self, node: Node):

        if not self.node:
            self.node = node

        elif node < self.node:
            self.node.left._insert(node)

        elif node > self.node:
            self.node.right._insert(node)

        else:
            raise NodeTreeDuplicateError(f"Node {node.key} is already in tree.")

    def _delete(self):
        if self.node is not None:
            if self.left_node is None and self.right_node is None:
                self.node = None

            elif self.right_node is None:
                self.node = self.left_node

            elif self.left_node is None:
                self.node = self.right_node

            else:
                successor = self.successor()
                self.node.replace(successor.node)
                successor.node = None

    def insert(self, node: Node):
        print(f"Insert node {node.key}")
        self._insert(node)

    def delete(self):
        print(f"Delete node {self.node.key}")
        self.delete()

    def smallest_child(self):
        if self.left_node is None:
            return self

        return self.left_tree.smallest_child()

    def biggest_child(self):
        if self.right_node is None:
            return self

        return self.right_tree.biggest_child()

    def successor(self):
        if self.right_node is not None:
            return self.right_tree.smallest_child()
        else:
            return self.left_tree.biggest_child()

    def rotate_left(self):
        print(f"Left rotation node {self.node.key}")
        root_node = self.node
        pivot_node = self.right_node

        if pivot_node is None:
            raise NodeTreeRotationError("No pivot node to rotate.")

        pivot_left_node = self.right_tree.left_node

        root_node.right.node = pivot_left_node
        pivot_node.left.node = root_node
        self.node = pivot_node

    def rotate_right(self):
        print(f"Right rotation node {self.node.key}")
        root_node = self.node
        pivot_node = self.left_node

        if pivot_node is None:
            raise NodeTreeRotationError("No pivot node to rotate.")

        pivot_right_node = self.left_tree.right_node

        root_node.left.node = pivot_right_node
        pivot_node.right.node = root_node
        self.node = pivot_node

    def rotate_left_left(self):
        self.rotate_left()
        self.rotate_left()

    def rotate_left_right(self):
        self.rotate_left()
        self.rotate_right()

    def rotate_right_left(self):
        self.rotate_right()
        self.rotate_left()

    def rotate_right_right(self):
        self.rotate_right()
        self.rotate_right()

    def balance_node(self):
        if self.is_balanced:
            print(f"Node {self.node.key} is balanced")
            return

        if self.balance_factor < -1:
            self.rotate_right()
        else:
            self.rotate_left()

    def balance_tree(self):
        if self.left_node:
            self.left_tree.balance_tree()

        if self.right_node:
            self.right_tree.balance_tree()

        if not self.is_balanced:
            print(f"Balancing node {self.node.key}")
            self.balance_node()


tree = NodeTree()

with open("/home/alex/PycharmProjects/kpi/data_structure/BinTree10.txt") as fd:
    for line in fd.readlines():
        k, v = line.strip().split(maxsplit=1)
        next_node = Node(int(k), v)
        tree._insert(next_node)

print(tree.display())
tree.balance_tree()
print(tree.display())
tree.balance_tree()
