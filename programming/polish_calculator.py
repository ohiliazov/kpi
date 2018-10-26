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

MATH_CONSTANTS = {
    "e": math.e,
    "pi": math.pi
}

BINARY_OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '−': operator.sub,
    '*': operator.mul,
    '×': operator.mul,
    '/': operator.truediv,
    '//': operator.floordiv,
    '%': operator.mod,
    '^': operator.pow,
    'log': math.log,
}

UNARY_OPERATORS = {
    "!": math.factorial,
    "sin": math.sin,
    "cos": math.cos,
    "exp": math.exp,
    "tan": math.tan
}


class EquationException(Exception):
    pass


class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    @property
    def size(self):
        return len(self.items)


class PolishCalculator:
    def __init__(self):
        self.op_counter = 0
        self.stack = Stack()

    def _reset(self):
        self.op_counter = 0
        self.stack = Stack()

    def calculate(self, math_equation):
        self._reset()

        for element in math_equation.split():
            if element in MATH_CONSTANTS:
                self.push_to_stack(MATH_CONSTANTS[element])

            elif element in UNARY_OPERATORS:
                self.unary_operation(element)

            elif element in BINARY_OPERATORS:
                self.binary_operation(element)

            else:
                self.push_to_stack(element)

        if self.stack.size != 1:
            print(f"Stack: {self.stack.items}")
            raise EquationException("Stack has more than one element")

        return self.stack.peek()

    def push_to_stack(self, item):
        try:
            self.stack.push(float(item))
        except ValueError:
            raise EquationException(f"Invalid character: {item}")

    def binary_operation(self, op):
        if self.stack.size < 2:
            raise EquationException("Not enough items in stack for binary operation.")

        right = self.stack.pop()
        left = self.stack.pop()

        result = BINARY_OPERATORS[op](left, right)
        self.stack.push(result)
        self.op_counter += 1

        print(f"{self.op_counter}. {left:.2f} {op} {right:.2f} = {result:.2f}")

    def unary_operation(self, op):
        if self.stack.size < 1:
            raise EquationException("No items in stack.")

        num = self.stack.pop()

        result = UNARY_OPERATORS[op](num)
        self.stack.push(result)
        self.op_counter += 1

        print(f"{self.op_counter}. {num:.2f} {op} = {result:.2f}")


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
    calc = PolishCalculator()

    for k, v in valid_strings.items():
        assert calc.calculate(k) == v


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
    calc = PolishCalculator()

    for s in invalid_strings:
        try:
            calc.calculate(s)

        except EquationException:
            pass
        else:
            raise AssertionError("Test failed on: %s" % s)


if __name__ == '__main__':
    calc = PolishCalculator()

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
                result = calc.calculate(equation)
                print("\nEquation result: %.2f\n" % result)

        except (EquationException, IOError) as e:
            print(e)
            pass
