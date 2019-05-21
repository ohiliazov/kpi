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

    def get_derivative_polynomial(self):
        res = []
        for index, coeff in enumerate(self.coefficients):
            res.append(index * coeff)

        return Polynomial(*res[:0:-1])

    def get_sturm_array(self):
        res = []
        coeff = self.coefficients[::-1]
        while coeff:
            p = Polynomial(*coeff)
            res.append(p)
            coeff = p.get_derivative_polynomial().coefficients[::-1]

        return res[:-1]

    def print_sturm(self, a, b, step=1.0):
        for p in self.get_sturm_array():

            for x in np.arange(a, b, step):

                res = p(x)
                if res > 0:
                    print('+', end=' ')
                elif res < 0:
                    print('-', end=' ')
                else:
                    print('0', end=' ')

            print()


if __name__ == '__main__':
    p = Polynomial(0, -1, 3, 0, -2, 2)
    X = np.linspace(-1.1, 2.9, endpoint=True)
    p.print_sturm(-4, 4, .25)

    for pol in p.get_sturm_array():
        F = pol(X)
        plt.plot(X, F)

    plt.ylim((-24, 10))
    plt.show()
