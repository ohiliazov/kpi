import math
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
                    print('+', end='')
                elif res < 0:
                    print('-', end='')
                else:
                    print('0', end='')

            print()


def bisection_method(polynomial: Polynomial, a: float, b: float, epsilon: float = 0.00001):
    print("\n====== BISECTION METHOD ======\n")
    x_left = polynomial(a)
    x_right = polynomial(b)

    assert x_left < 0 < x_right or x_left > 0 > x_right

    is_ascending = x_right > 0

    i = 0
    while True:
        print(f'Iter {i}: '
              f'a = {round(a, 6)}; F(a) = {round(x_left, 6)}; '
              f'b = {round(b, 6)}; F(b) = {round(x_right, 6)}')

        c = (a + b) / 2
        fx = polynomial(c)

        if -epsilon < fx < epsilon or abs(a - b) < epsilon or math.isclose(fx, 0, rel_tol=epsilon):
            print(f"\n====== X = {round(c, 6)} ======")
            return round(c, 6)

        if fx < 0 and is_ascending or fx > 0 and not is_ascending:
            a, x_left = c, fx
        else:
            b, x_right = c, fx

        i += 1


def secant_method(polynomial: Polynomial, a: float, b: float, epsilon: float = 0.00001):
    print("\n====== SECANT METHOD ======\n")
    x_left = polynomial(a)
    x_right = polynomial(b)

    assert x_left < 0 < x_right or x_left > 0 > x_right

    is_ascending = x_right > 0

    i = 0
    while True:
        print(f'Iter {i}: '
              f'a = {round(a, 6)}; F(a) = {round(x_left, 6)}; '
              f'b = {round(b, 6)}; F(b) = {round(x_right, 6)}')

        c = (a * x_right - b * x_left) / (x_right - x_left)
        fx = polynomial(c)

        if -epsilon < fx < epsilon or abs(a - b) < epsilon:
            print(f"\n====== X = {round(c, 6)} ======")
            return round(c, 6)

        if fx < 0 and is_ascending or fx > 0 and not is_ascending:
            a, x_left = c, fx
        else:
            b, x_right = c, fx

        i += 1


def newton_method(polynomial: Polynomial, x: float, epsilon=0.00001):
    print("\n====== NEWTON METHOD ======\n")
    i = 0
    while True:
        fx = polynomial(x)
        print(f'Iter {i}: F({round(x, 6)}) = {round(fx, 6)}')

        if -epsilon < fx < epsilon:
            print(f"\n====== X = {round(x, 6)} ======")
            return round(x, 6)

        x = x - fx / polynomial.derivative(x)
        i += 1


if __name__ == '__main__':
    p = Polynomial(0, -1, 3, 0, -2, 2)
    X = np.linspace(-4, 4, num=200, endpoint=True)

    F = p(X)
    plt.plot(X, F)
    ax = plt.axes()  # type: plt.Axes
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.grid(True)
    plt.xlim((-4, 4))
    plt.ylim((-10, 10))
    plt.show()
    print("====== -x^4 + 3*x^3 - 2*x + 2 ======")

    bisection_left = bisection_method(p, -2, -2 / 5)
    bisection_right = bisection_method(p, 2, 3)

    secant_left = secant_method(p, -2, -2 / 5)
    secant_right = secant_method(p, 2, 3)

    newton_left = newton_method(p, -2)
    newton_right = newton_method(p, 3)

    print(
        f"\n===== RESULTS =====\n\n"
        f"BISECTION: {bisection_left, bisection_right}\n"
        f"SECANT: {secant_left, secant_right}\n"
        f"NEWTON: {newton_left, newton_right}\n"
    )
