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

    def _load(self, item):
        """ Load a number to stack
        1. Convert a
        :param item: string that represents float number
        """
        try:
            item = float(item)
        except ValueError:
            raise EquationException(f"Invalid character: {item}")

        self.stack.push(item)

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

        result = BINARY_OPERATORS[op](c, b)
        self.stack.push(result)
        self.op_counter += 1

        print(f"{self.op_counter}. {c:.2f} {op} {b:.2f} = {result:.2f}")

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
        self.stack.push(result)
        self.op_counter += 1

        print(f"{self.op_counter}. {a:.2f} {op} = {result:.2f}")

    def calculate(self, math_equation):
        self._reset()

        for element in math_equation.split():
            if element in MATH_CONSTANTS:
                self._load(MATH_CONSTANTS[element])

            elif element in UNARY_OPERATORS:
                self._unary(element)

            elif element in BINARY_OPERATORS:
                self._binary(element)

            else:
                self._load(element)

        if self.stack.size != 1:
            print(f"Stack: {self.stack.items}")
            raise EquationException("Stack has more than one element")

        return self.stack.peek()


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
