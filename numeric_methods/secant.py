from . import Polynomial


def secant_method(polynomial: Polynomial, a: float, b: float, epsilon: float = 0.00001):
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

        if -epsilon < fx < epsilon:
            return c

        if fx < 0 and is_ascending or fx > 0 and not is_ascending:
            a, x_left = c, fx
        else:
            b, x_right = c, fx

        i += 1
