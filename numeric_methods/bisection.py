"""
Formula: 0*(1-0)*x^5 + (-1)*x^4 + 3*x^3 + 0*x^2 + (-2)*x + 2*1 = 0
Formula: -x^4 + 3*x^3 - 2x + 2 = 0
alpha = 0
k = 2
epsilon = 0.00001
"""
from . import Polynomial


def bisection_method(polynomial: Polynomial, a: float, b: float, epsilon: float = 0.00001):
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

        if -epsilon < fx < epsilon:
            return c

        if fx < 0 and is_ascending or fx > 0 and not is_ascending:
            a, x_left = c, fx
        else:
            b, x_right = c, fx

        i += 1
