import operator
import sys

OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '//': operator.floordiv,
    '%': operator.mod,
    '^': operator.pow,
    '**': operator.pow
}


def validate_equation(equation: list):
    """ Checks if equation is correct. Returns ValueError with info """
    if not equation:
        raise ValueError("Incorrect equation: No elements are given")

    if equation[0] in OPERATORS:
        raise ValueError("Incorrect equation: First element is operator")

    diff_count = 0

    for item in equation:
        if item in OPERATORS.keys():
            diff_count -= 1
        elif float(item):
            diff_count += 1

        if diff_count < 1:
            raise ValueError("Incorrect equation: Too many operators")

    if diff_count > 1:
        raise ValueError("Incorrect equation: Too many operands")


def execute_operation(x, y, op):
    return OPERATORS[op](x, y)


def rpn_calculate(equation: list):
    stack = []
    counter = 1
    for item in equation:
        if item in OPERATORS:
            y = stack.pop()
            x = stack.pop()
            res = execute_operation(x, y, item)
            stack.append(res)
            print("Step %d: %.2f %s %.2f = %.2f" % (counter, x, item, y, res))
        else:
            stack.append(float(item))
            print("Step %d: add %s to stack" % (counter, item))

        print("Stack: %s\n" % stack)
        counter += 1

    return stack.pop()


if __name__ == "__main__":
    if sys.argv[1:]:
        equation = sys.argv[1:]
    else:
        input_string = input("Enter RPN equation: ")
        equation = input_string.split()

    validate_equation(equation)
    result = rpn_calculate(equation)
    print("RESULT: %.2f" % result)
