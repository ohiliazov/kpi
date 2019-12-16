import numpy as np
from scipy import stats


def laplace(value: float):
    return stats.norm.pdf(value)


def inverted_laplace(value: float):
    return 1 / laplace(value)


print(laplace(1.1))
print(inverted_laplace(1.1))

expenses = np.array([
    [9, 3, 6, 10]
])

consumers = np.array([
    [5, 3, 6, 2],
    [3, 4, 5, 6],
    [7, 5, 6, 4],
    [4, 8, 5, 3],
])

max_volumes = np.array([
    [400],
    [800],
    [200],
    [800],
])

boundaries = np.array([
    [300, 500],
    [700, 1000],
    [200, 400],
    [600, 1000],
])

penalty_low = np.array([
    [8],
    [10],
    [19],
    [6],
])

penalty_high = np.array([
    [5],
    [6],
    [6],
    [3],
])
