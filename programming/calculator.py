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


def calculate(math_equation: str):
    stack = []

    for s in math_equation.split():
        if s in math_constants:
            stack.append(math_constants[s])

        elif s in binary_ops:

            if len(stack) < 2:
                raise BadEquationError("Not enough numbers.")

            a, b = stack.pop(), stack.pop()

            operation = binary_ops[s](b, a)

            stack.append(operation)
        elif s in unary_ops:

            if not stack:
                raise BadEquationError("Not enough numbers.")

            a = stack.pop()

            operation = unary_ops[s](a)

            stack.append(operation)
        else:
            try:
                stack.append(int(s))
            except ValueError:
                raise BadEquationError("Invalid character: %s" % s)

    if len(stack) > 1:
        raise BadEquationError("Too many numbers in stack left: %s " % stack)

    result = stack.pop()

    print("%s is %s" % (math_equation, result))
    return result


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
            equation = input("Enter equation RPN: ")

            if equation in ["", "quit", "exit", "close"]:
                break

            elif equation == 'test':
                test_valid()
                test_invalid()
            else:
                calculate(equation)

        except BadEquationError as e:
            print(e)
            pass
