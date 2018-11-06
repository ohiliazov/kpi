""" UNION FIND
M - number of union-find operations
N - number of objects
"""


class QuickFind:
    """ Quick-find
     Worst case time: M * N """

    def __init__(self, n):
        self.ids = []

        for i in range(n):
            self.ids.append(i)

    def connected(self, p, q):
        return self.ids[p] == self.ids[q]

    def union(self, p, q):
        if not self.connected(p, q):
            pid = self.ids[p]
            qid = self.ids[q]

            for i in range(len(self.ids)):
                if self.ids[i] == pid:
                    self.ids[i] = qid


class QuickUnion:
    """ Quick-union
     Worst case time: M * N """

    def __init__(self, n):
        self.ids = []

        for i in range(n):
            self.ids.append(i)

    def root(self, i):
        while i != self.ids[i]:
            i = self.ids[i]

        return i

    def connected(self, p, q):
        return self.root(p) == self.root(q)

    def union(self, p, q):
        i = self.root(p)
        j = self.root(q)

        if i != j:
            self.ids[i] = j


class WeightedQuickUnion:
    """ Weighted quick-union
     Worst case time: N + M log N """

    def __init__(self, n):
        self.ids = []
        self.sz = []

        for i in range(n):
            self.ids.append(i)
            self.sz.append(1)

    def root(self, i):
        while i != self.ids[i]:
            i = self.ids[i]

        return i

    def connected(self, p, q):
        return self.root(p) == self.root(q)

    def union(self, p, q):
        i = self.root(p)
        j = self.root(q)

        if i == j:
            return

        if self.sz[i] < self.sz[j]:
            self.ids[i] = j
            self.sz[j] += self.sz[i]
        else:
            self.ids[j] = i
            self.sz[i] += self.sz[j]


class QuickUnionPathCompression:
    """ Quick-union + path compression
     Worst case time: N + M log N """

    def __init__(self, n):
        self.ids = []

        for i in range(n):
            self.ids.append(i)

    def root(self, i):
        while i != self.ids[i]:
            i = self.ids[i] = self.ids[self.ids[i]]

        return i

    def connected(self, p, q):
        return self.root(p) == self.root(q)

    def union(self, p, q):
        i = self.root(p)
        j = self.root(q)

        if i != j:
            self.ids[i] = j


class WeightedQuickUnionPathCompression:
    """ Weighted quick-union + path compression
     Worst case time: N + M lg* N """

    def __init__(self, n):
        self.ids = []
        self.sz = []

        for i in range(n):
            self.ids.append(i)
            self.sz.append(1)

    def root(self, i):
        while i != self.ids[i]:
            i = self.ids[i] = self.ids[self.ids[i]]

        return i

    def connected(self, p, q):
        return self.root(p) == self.root(q)

    def union(self, p, q):
        i = self.root(p)
        j = self.root(q)

        if i == j:
            return

        if self.sz[i] < self.sz[j]:
            self.ids[i] = j
            self.sz[j] += self.sz[i]
        else:
            self.ids[j] = i
            self.sz[i] += self.sz[j]
