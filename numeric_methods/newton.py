from . import Polynomial


def newton_method(polynomial: Polynomial, x: float, epsilon=0.00001):
    i = 0
    while True:
        fx = polynomial(x)
        print(f'Iter {i}: F({round(x, 6)}) = {round(fx, 6)}')

        if -epsilon < fx < epsilon:
            return x

        x = x - fx / polynomial.derivative(x)
        i += 1
