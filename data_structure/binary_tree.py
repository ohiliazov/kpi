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


class NodeTree:
    def __init__(self, *args):
        self.node = None

        if args:
            for node in args:
                self.insert(node)

    def __repr__(self):
        return f"{self.node}"

    @property
    def left(self):
        return self.node.left_child

    @property
    def right(self):
        return self.node.right_child

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
            if not (self.left or self.right):
                self.node = None

            elif not self.right:
                self.node = self.left.node

            elif not self.left:
                self.node = self.right.node

            else:
                raise NotImplementedError()

    def rotate_left(self):
        root_node = self.node
        pivot_node = self.right.node

        if pivot_node is None:
            raise NodeTreeRotationError("No pivot node to rotate.")

        pivot_left_node = self.right.left.node

        root_node.right_child.node = pivot_left_node
        pivot_node.left_child.node = root_node
        self.node = pivot_node

    def rotate_right(self):
        root_node = self.node
        pivot_node = self.left.node

        if pivot_node is None:
            raise NodeTreeRotationError("No pivot node to rotate.")

        pivot_right_node = self.left.right.node

        root_node.left_child.node = pivot_right_node
        pivot_node.right_child.node = root_node
        self.node = pivot_node


tree = NodeTree()

with open("/home/alex/PycharmProjects/kpi/data_structure/BinTree10.txt") as fd:
    for line in fd.readlines():
        k, v = line.strip().split(maxsplit=1)
        next_node = Node(int(k), v)
        tree.insert(next_node)

print(tree)
