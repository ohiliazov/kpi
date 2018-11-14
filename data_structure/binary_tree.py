import os


class NodeTreeDuplicateError(KeyError):
    pass


class NodeTreeRotationError(KeyError):
    pass


class Node:
    def __init__(self, key: int, value: str = None):
        self.key = key
        self.value = value
        self.left_child = NodeTree()
        self.right_child = NodeTree()

    def __repr__(self):
        return f"{self.key}"

    def __lt__(self, other: "Node"):
        return self.key < other.key

    def __gt__(self, other: "Node"):
        return self.key > other.key

    def replace(self, node: "Node"):
        self.key = node.key
        self.value = node.value


class NodeTree:
    def __init__(self, *args):
        self.node = None

        if args:
            for node in args:
                self.insert(node)

    def __repr__(self):
        return f"{self.node}"

    @property
    def left_tree(self):
        if self.node:
            return self.node.left_child

    @property
    def left_node(self):
        return self.left_tree.node

    @property
    def right_tree(self):
        if self.node:
            return self.node.right_child

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
            return 0

        if self.left_node is None:
            return self.right_tree.height

        if self.right_node is None:
            return -self.left_tree.height

        return self.right_tree.height - self.left_tree.height

    def is_balanced(self):
        return -2 < self.balance_factor < 2

    def insert(self, node: Node):
        if not self.node:
            self.node = node

        elif node < self.node:
            self.node.left_child.insert(node)

        elif node > self.node:
            self.node.right_child.insert(node)

        else:
            raise NodeTreeDuplicateError(f"Node {node.key} is already in tree.")

    def delete(self):
        if self.node is not None:
            if self.left_node is None and self.right_node is None:
                self.node = None

            elif self.right_node is None:
                self.node = self.left_node

            elif self.left_node is None:
                self.node = self.right_node

            else:
                successor = self.right_tree.successor()
                self.node.replace(successor.node)
                successor.node = None

    def successor(self):
        if self.left_node is None:
            return self

        return self.left_tree.successor

    def rotate_left(self):
        root_node = self.node
        pivot_node = self.right_node

        if pivot_node is None:
            raise NodeTreeRotationError("No pivot node to rotate.")

        pivot_left_node = self.right_tree.left_node

        root_node.right_child.node = pivot_left_node
        pivot_node.left_child.node = root_node
        self.node = pivot_node

    def rotate_right(self):
        root_node = self.node
        pivot_node = self.left_node

        if pivot_node is None:
            raise NodeTreeRotationError("No pivot node to rotate.")

        pivot_right_node = self.left_tree.right_node

        root_node.left_child.node = pivot_right_node
        pivot_node.right_child.node = root_node
        self.node = pivot_node


tree = NodeTree()

with open(os.path.abspath("./BinTree10.txt")) as fd:
    for line in fd.readlines():
        k, v = line.strip().split(maxsplit=1)
        next_node = Node(int(k), v)
        tree.insert(next_node)

print(tree)
tree.count_children