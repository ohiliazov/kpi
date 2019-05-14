"""
Курсова робота

Тема: Калькулятор.
За заданим символьним рядком з математичною формулою обчислити значення
функції в заданій точці (з використанням польського інверсного запису)

Виконав: Гілязов Олександр Ігорович
Група: ІС-зп81
"""

import math
import operator

# Тут задаються символи, які калькулятор буде розпізнавати
binary_ops = {
    '+': operator.add,
    '-': operator.sub,
    '−': operator.sub,
    '*': operator.mul,
    '×': operator.mul,
    '/': operator.truediv,
    '//': operator.floordiv,
    '%': operator.mod,
    '^': operator.pow,
    "log": math.log,
}

unary_ops = {
    "sin": math.sin,
    "cos": math.cos,
    "!": math.factorial,
    "exp": math.exp
}

math_constants = {
    "e": math.e,
    "pi": math.pi
}


class BadEquationError(Exception):
    pass


def binary_operation(stack, op):
    if len(stack) < 2:
        raise BadEquationError("Not enough numbers.")

    a, b = stack.pop(), stack.pop()

    res = binary_ops[op](b, a)
    print("Evaluating: %.2f %s %.2f = %.2f" % (b, op, a, res))

    return res


def unary_operation(stack, op):
    if not stack:
        raise BadEquationError("Not enough numbers.")

    a = stack.pop()
    res = unary_ops[op](a)
    print("Evaluating: %.2f %s = %.2f" % (a, op, res))

    return res


def add_to_stack(stack, s):
    try:
        stack.append(float(s))
    except ValueError:
        raise BadEquationError("Cannot process equation at point: %s" % s)


def calculate(math_equation: str):
    stack = []

    for s in math_equation.split():
        if s in math_constants:
            stack.append(math_constants[s])

        elif s in binary_ops:
            op = binary_operation(stack, s)
            stack.append(op)

        elif s in unary_ops:
            op = unary_operation(stack, s)
            stack.append(op)

        else:
            add_to_stack(stack, s)

    if len(stack) > 1:
        raise BadEquationError("Too many numbers in stack left: %s " % stack)

    return stack.pop()


def test_valid():
    valid_strings = {
        "1 1 +": 2,
        "2 3 -": -1,
        "4 5 *": 20,
        "5 2 /": 2.5,
        "7 2 //": 3,
        "9 2 ^": 81,
        "11 12 13 + *": 275,
        "1 2 + 4 × 5 + 3 −": 14
    }

    for k, v in valid_strings.items():
        assert calculate(k) == v


def test_invalid():
    invalid_strings = [
        "- 1",
        "+ 2",
        "* 3",
        "/ 4 5",
        "^ 6",
        "7 8",
        "9 10 + -",
        "11 12 * /",
        "13 14 &",
        "a b c + +"
    ]

    for s in invalid_strings:
        try:
            calculate(s)

        except BadEquationError as ex:
            print("Exception raised: %s" % ex)
            pass

        else:
            raise AssertionError("Test failed on: %s" % s)


if __name__ == '__main__':
    while True:
        try:
            equation = input("Enter equation (using RPN): ")
            print()

            if equation in ["", "quit", "exit", "close"]:
                break

            elif equation == 'test':
                test_valid()
                test_invalid()
            else:
                result = calculate(equation)
                print("\nEquation result: %.2f\n" % result)

        except BadEquationError as e:
            print(e)
            pass
