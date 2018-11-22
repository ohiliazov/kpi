import argparse
import os
import sys


class Node:
    def __init__(self, key: int, value: str = None):
        self.key = int(key)
        self.value = value
        self.left = NodeTree()
        self.right = NodeTree()

    def __str__(self):
        return f"{self.key} {self.value}"

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

    def __str__(self):
        return self.display()

    def __getitem__(self, item):
        t = self._find(item)
        if t:
            return t.node.value

    def __delitem__(self, key):
        t = self._find(key)
        if t:
            t._delete()

    def display(self, depth=0):
        indent = "    " * depth
        result = f"{indent}{self.node}\n"

        if self.node.left.node:
            result += self.node.left.display(depth + 1)

        if self.node.right.node:
            result += self.node.right.display(depth + 1)

        return result

    def _find(self, key: int):
        key = int(key)
        if key == self.node.key:
            return self

        elif key < self.node.key and self.node.left.node:
            return self.node.left._find(key)

        elif key > self.node.key and self.node.right.node:
            return self.node.right._find(key)

    @property
    def is_balanced(self):
        balanced = -2 < self.balance_factor < 2

        if self.node.left.node:
            balanced = balanced and self.node.left.is_balanced

        if self.node.right.node:
            balanced = balanced and self.node.right.is_balanced

        return balanced

    @property
    def height(self):
        height = 1
        height_left = self.node.left.height if self.node.left.node else 0
        height_right = self.node.right.height if self.node.right.node else 0

        return height + max(height_left, height_right)

    @property
    def balance_factor(self):
        balance_factor = 0

        if self.node.left.node:
            balance_factor -= self.node.left.height

        if self.node.right.node:
            balance_factor += self.node.right.height

        return balance_factor

    def _insert(self, node: Node):
        if not self.node:
            self.node = node

        elif node < self.node:
            self.node.left._insert(node)

        elif node > self.node:
            self.node.right._insert(node)

        else:
            print(f"Duplicate: {node.key}")

    def _delete(self):
        if self.node is not None:
            if self.node.left.node is None and self.node.right.node is None:
                self.node = None

            elif self.node.right.node is None:
                self.node = self.node.left.node

            elif self.node.left.node is None:
                self.node = self.node.right.node

            else:
                successor = self.node.right._successor()
                self.node.replace(successor.node)
                successor.node = successor.node.right.node

    def _successor(self):
        if self.node.left.node is None:
            return self

        return self.node.left._successor()

    def _rotate_left(self):
        root_node = self.node
        pivot_node = self.node.right.node

        if pivot_node:
            pivot_left_node = self.node.right.node.left.node
            root_node.right.node = pivot_left_node
            pivot_node.left.node = root_node
            self.node = pivot_node

    def _rotate_right(self):
        root_node = self.node
        pivot_node = self.node.left.node

        if pivot_node:
            pivot_right_node = self.node.left.node.right.node
            root_node.left.node = pivot_right_node
            pivot_node.right.node = root_node
            self.node = pivot_node

    def _balance(self):
        if self.balance_factor < -1:
            if self.node.left.balance_factor > 0:
                self.node.left._rotate_left()
            self._rotate_right()
        elif self.balance_factor > 1:
            if self.node.right.balance_factor < 0:
                self.node.right._rotate_right()
            self._rotate_left()

    def _balance_tree(self):
        while not self.is_balanced:
            if self.node.left.node:
                self.node.left._balance_tree()

            if self.node.right.node:
                self.node.right._balance_tree()

            self._balance()


class NodeTreeFacade(NodeTree):
    def find(self, key):
        t = self._find(key)
        if t:
            print(t.node.value)
        else:
            print(f"Not found: {key}")

    def insert(self, node: Node):
        print(f"Insert: {node.key}")
        self._insert(node)

    def delete(self, key=None):
        t = self._find(key or self.node.key)
        print(f"Delete: {t.node.key}")
        t._delete()

    def rotate_left(self, key=None):
        t = self._find(key or self.node.key)
        print(f"Left rotation: {t.node.key}")
        t._rotate_left()

    def rotate_right(self, key=None):
        t = self._find(key or self.node.key)
        print(f"Right rotation: {t.node.key}")
        t._rotate_right()

    def rotate_left_left(self, key=None):
        t = self._find(key or self.node.key)
        print(f"Double left rotation: {t.node.key}")
        t._rotate_left()
        t._rotate_left()

    def rotate_right_right(self, key=None):
        t = self._find(key or self.node.key)
        print(f"Double right rotation: {t.node.key}")
        t._rotate_right()
        t._rotate_right()

    def rotate_left_right(self, key=None):
        t = self._find(key or self.node.key)
        print(f"Left right rotation: {t.node.key}")
        t._rotate_left()
        t._rotate_right()

    def rotate_right_left(self, key=None):
        t = self._find(key or self.node.key)
        print(f"Right left rotation: {t.node.key}")
        t._rotate_right()
        t._rotate_left()

    def balance_tree(self, key=None):
        t = self._find(key or self.node.key)
        print(f"Balance tree: {t.node.key}")
        t._balance_tree()


def parse_cmd_line():
    parser = argparse.ArgumentParser(argument_default=None)

    parser.add_argument("bt_path", help="Path to binary tree input")

    return parser.parse_args()


def parse_input(tree, command):
    cmd = command.split(" ")

    while len(cmd) < 3:
        cmd.append(None)

    if cmd[0] in ['close', 'exit', 'quit']:
        print("Exit")
        sys.exit(0)

    if cmd[0] in ['add', 'insert'] and cmd[1]:
        tree.insert(Node(cmd[1], cmd[2]))

    elif cmd[0] in ['get'] and cmd[1]:
        print(f"Key: {cmd[1]} Value: {tree[cmd[1]]}")

    elif cmd[0] in ['del', 'delete']:
        tree.delete(cmd[1])

    elif cmd[0] in ['l', 'left', 'rotate_left']:
        tree.rotate_left(cmd[1])

    elif cmd[0] in ['r', 'right', 'rotate_right']:
        tree.rotate_right(cmd[1])

    elif cmd[0] in ['ll', 'left_left', 'double_rotate_left']:
        tree.rotate_left_left(cmd[1])

    elif cmd[0] in ['rr', 'right_right', 'double_rotate_right']:
        tree.rotate_right_right(cmd[1])

    elif cmd[0] in ['lr', 'left_right', 'rotate_left_right']:
        tree.rotate_left_right(cmd[1])

    elif cmd[0] in ['rl', 'right_left', 'rotate_right_left']:
        tree.rotate_right_left(cmd[1])

    elif cmd[0] in ['balance']:
        tree.balance_tree(cmd[1])

    elif cmd[0] in ['print', 'display']:
        print(tree.display())
    elif cmd[0] in ['save'] and cmd[1]:
        with open(os.path.abspath(cmd[1]), mode='w') as fd:
            fd.write(tree.display())
    else:
        print(f"Unknown or incorrect command: {cmd}")


if __name__ == "__main__":
    bt_path = parse_cmd_line().bt_path

    tree = NodeTreeFacade()
    with open(os.path.abspath(bt_path)) as fd:
        for line in fd.readlines():
            k, v = line.strip().split(maxsplit=1)
            next_node = Node(int(k), v)
            tree.insert(next_node)

    print(tree.display())

    while True:
        cmd = input("Write command: ")
        parse_input(tree, cmd)
