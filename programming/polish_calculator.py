"""
Курсова робота

Тема: Калькулятор.
За заданим символьним рядком з математичною формулою обчислити значення
функції в заданій точці (з використанням польського інверсного запису)

Виконав: Гілязов Олександр Ігорович
Група: ІС-зп81
"""

import argparse
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
        """ Initialize stack and operation counter """
        self.stack = Stack()
        self.op_counter = 0

    def _reset(self):
        """ Reset stack and operation counter """
        self.stack = Stack()
        self.op_counter = 0

    def _push_to_stack(self, item):
        """ Load a number to stack
        1. Convert a
        :param item: string that represents float number
        """
        try:
            item = float(item)
        except ValueError:
            raise EquationException(f"Invalid character: {item}")

        self.stack.push(item)
        print(f"ADD TO STACK: {item:.2f}")

    def _binary(self, op):
        """ Binary operation:
        1. Take two numbers from stack
        2. Perform binary operation on them
        3. Push result to stack

        :param item: string that represents binary operator
        """
        if self.stack.size < 2:
            raise EquationException("Not enough items in stack for binary operation.")

        b = self.stack.pop()
        c = self.stack.pop()

        try:
            result = BINARY_OPERATORS[op](c, b)
        except ZeroDivisionError:
            raise EquationException(f"Cannot divide by zero: {c:.2f} {op} {b:.2f}")

        self.op_counter += 1
        print(f"OPERATION {self.op_counter}: {c:.2f} {op} {b:.2f} = {result:.2f}")
        self._push_to_stack(result)

    def _unary(self, op):
        """ Unary operation:
        1. Take one number from stack
        2. Perform unary operation on it
        3. Push result to stack

        :param item: string that represents unary operator
        """
        if self.stack.size < 1:
            raise EquationException("No items in stack.")

        a = self.stack.pop()
        result = UNARY_OPERATORS[op](a)

        self.op_counter += 1
        print(f"OPERATION {self.op_counter}: {a:.2f} {op} = {result:.2f}")
        self._push_to_stack(result)

    def calculate(self, math_equation):
        self._reset()

        if isinstance(math_equation, str):
            math_equation = math_equation.split()

        print(f"EQUATION: {' '.join(math_equation)}")
        for element in math_equation:

            if element in MATH_CONSTANTS:
                self._push_to_stack(MATH_CONSTANTS[element])

            elif element in UNARY_OPERATORS:
                self._unary(element)

            elif element in BINARY_OPERATORS:
                self._binary(element)

            else:
                self._push_to_stack(element)

            print(f"\nSTACK: {[round(item, 2) for item in self.stack.items]}")

        if self.stack.size != 1:
            raise EquationException("Stack has more than one element")

        result = self.stack.peek()
        print(f"RESULT: {result:.2f}\n\n")
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
        "1 2 + 4 × 5 + 3 −": 14,
        "3 4 2 * 1 5 − 2 ^ / +": 3.5
    }
    calc = PolishCalculator()

    for k, v in valid_strings.items():
        assert calc.calculate(k) == v


def test_invalid():
    invalid_strings = [
        "1 0 /",
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

        except EquationException as exc:
            print(f"EXCEPTION: {exc}")
            pass
        else:
            raise AssertionError("Test failed on: %s" % s)


def parse_equation_arg():
    parser = argparse.ArgumentParser(argument_default=None)
    parser.add_argument('equation', nargs='*', help='Specific providers list')

    return parser.parse_known_args()[0].equation


if __name__ == '__main__':
    calc = PolishCalculator()

    equation = parse_equation_arg()

    if equation:
        result = calc.calculate(equation)
        exit(0)

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

        except (EquationException, IOError) as exc:
            print(f"EXCEPTION: {exc}\n")
            pass
