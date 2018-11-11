import os


class Node:
    def __init__(self, data):
        self.key = int(data[0])
        self.description = data[1]
        self.left = None
        self.right = None

    def __repr__(self):
        return f"{self.key} {self.description}"

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

    def add_node(self, node):
        if self > node:
            if not self.left:
                self.left = node
            else:
                self.left.add_node(node)
        elif self < node:
            if not self.right:
                self.right = node
            else:
                self.right.add_node(node)


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert_node(self, node: Node):
        if not self.root:
            self.root = node
        else:
            self.root.add_node(node)

    def find_node(self, key):
        parent = self.root
        if self.root.key == key:
            return self.root, None


data = []
with open(os.path.abspath('BinTree10.txt')) as fd:
    for line in fd.readlines():
        node = Node(line.strip().split(maxsplit=1))
        data.append(node)

print(data)

tree = BinaryTree()
for n in data:
    tree.insert_node(n)

print(tree)