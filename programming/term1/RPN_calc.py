import math
import sys

BINARY_OPERATORS = [
    "+",
    "-", "−",
    "*", "×",
    "/", "÷",
    "^", "**",
    "%",
    "//"
]

UNARY_OPERATORS = [
    "!",
    "sin",
    "cos",
    "tg", "tan",
    "cot", "cotan", "cotg", "ctg", "ctn",
    "sec",
    "csc", "cosec"
]


def push(stack: list, item: [str, float]):
    """ Converts item to float and pushes onto stack """
    item = float(item)  # raises ValueError if item cannot be converted

    stack.append(item)
    print(f"Pushed {item:.2f} onto stack")


def pop(stack: list):
    """ Removes last item while removing it from stack """
    if not stack:
        raise ValueError("Stack is empty")

    item = stack.pop()
    print(f"Popped {item:.2f} from stack")

    return item


def do_binary_math(stack: list, op: str):
    """ Pops two elements from stack, does math on them, and pushes the result onto stack """
    y = pop(stack)
    x = pop(stack)

    if op == "+":
        res = x + y

    elif op in ("-", "−"):
        res = x - y

    elif op in ("*", "×"):
        res = x * y

    elif op in ("/", "÷"):
        res = x / y

    elif op == "//":
        res = x // y

    elif op == "%":
        res = x % y

    elif op in ("^", "**"):
        res = x ** y

    else:
        raise NotImplementedError(f"Operator {op} is not supported")  # sanity check

    print(f"{x:.2f} {op} {y:.2f} = {res:.2f}")
    push(stack, res)


def do_unary_math(stack: list, op: str):
    """ Pops one element from stack, does math on it, and pushes the result onto stack """
    x = pop(stack)

    if op == "!":
        res = math.factorial(x)

    elif op == "sin":
        res = math.sin(x)
    elif op == "cos":
        res = math.cos(x)
    elif op in ("tg", "tan"):
        res = math.tan(x)

    elif op in ("cot", "cotan", "cotg", "ctg", "ctn"):
        res = 1 / math.tan(x)
    elif op == "sec":
        res = 1 / math.cos(x)
    elif op in ("csc", "cosec"):
        res = 1 / math.sin(x)

    else:
        raise NotImplementedError(f"Operator {op} is not supported")  # sanity check

    print(f"{x:.2f} {op} = {res:.2f}")
    push(stack, res)


def rpn_calculate(equation: list):
    stack = []

    for token in equation:

        if token in BINARY_OPERATORS:
            do_binary_math(stack, token)

        elif token in UNARY_OPERATORS:
            do_unary_math(stack, token)

        else:
            push(stack, token)

    if len(stack) != 1:
        raise AssertionError("Stack length is not equal to one")

    result = pop(stack)

    return result


def main():
    if len(sys.argv) > 1:
        equation = sys.argv[1:]

    else:
        input_string = input("Enter RPN equation: ")
        equation = input_string.split()

    result = rpn_calculate(equation)

    print(f"Result: {' '.join(equation)} => {result:.2f}")


if __name__ == "__main__":
    main()
