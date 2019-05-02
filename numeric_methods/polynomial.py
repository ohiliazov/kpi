import matplotlib.pyplot as plt
import numpy as np


class Polynomial:

    def __init__(self, *coefficients):
        self.coefficients = coefficients[::-1]

    def __repr__(self):
        return f"Polynomial" + str(self.coefficients[::-1])

    def __call__(self, x):
        res = 0
        for index, coeff in enumerate(self.coefficients):
            res += coeff * x ** index
        return res

    def derivative(self, x):
        res = 0
        for index, coeff in enumerate(self.coefficients):
            res += index * coeff * x ** (index - 1)
        return res


if __name__ == '__main__':
    p = Polynomial(0, -1, 3, 0, -2, 2)
    X = np.linspace(-1.1, 2.9, endpoint=True)
    F = p(X)
    plt.plot(X, F)
    plt.show()
