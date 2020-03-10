from collections import defaultdict
from pulp import *
from pprint import pprint
import math
print("===============================================================================================")
print("Вихідна задача з чіткими умовами")
print("===============================================================================================")
print("+-------------+------------------------------------+-------+\n"
      "|             | Завод 1  Завод 2  Завод 3  Завод 4 | Попит |\n"
      "+-------------+------------------------------------+-------+\n"
      "| Витрати     |    9        3        6       10    |       |\n"
      "+-------------+------------------------------------+-------+\n"
      "| Споживач 1  |    5        3        6        2    |  400  |\n"
      "| Споживач 2  |    3        4        5        6    |  800  |\n"
      "| Споживач 3  |    7        5        6        4    |  200  |\n"
      "| Споживач 4  |    4        8        5        3    |  800  |\n"
      "+-------------+------------------------------------+-------+\n"
      "| Потужність  |   500      700      600      ---   |       |\n"
      "| Дод.витрати |    3        2        5       ---   |       |\n"
      "+-------------+------------------------------------+-------+\n")


def solve_phase_one(consumers: int, producers: int,
                    transition_coeffs: list,
                    needs: list, powers: list):
    errors = []

    if len(transition_coeffs) != consumers * producers:
        errors.append("Транспортні витрати вказані невірно")

    if len(needs) != consumers:
        errors.append("Попит споживачів вказан невірно")

    if len(powers) != producers:
        errors.append("Потужність заводів вказана невірно")

    if errors:
        return errors

    X = []
    for i in range(consumers):
        for j in range(producers):
            X.append(pulp.LpVariable(f"X{i+1}{j+1}", lowBound=0, cat=pulp.LpInteger))

    transition_cost = sum([c_ij*x_ij for c_ij, x_ij in zip(transition_coeffs, X)])

    problem = pulp.LpProblem("0", LpMinimize)
    problem += transition_cost, "Цільова функція"

    print("Цільова функція:", transition_cost)

    # print("Обмеження за попитом:")
    # Обмеження за попитом
    for idx, need in enumerate(needs):
        # print(sum(X[producers*idx:producers*(idx+1)]) == need)
        problem += sum(X[producers*idx:producers*(idx+1)]) == need, f"споживач {idx + 1}"

    # print("Обмеження за потужністю:")
    for idx, power in enumerate(powers):
        # print(sum(X[idx::consumers]) <= power)
        problem += sum(X[idx::consumers]) <= power, f"завод {idx + 1}"

    problem.solve()

    print("План поставки:")
    for variable in problem.variables():
        if variable.varValue > 0:
            var_name = variable.name
            print(f"Завод {var_name[2]} -> Споживач {var_name[1]}: {int(variable.varValue)}")

    print(f"Витрати на транспортування: {int(value(transition_cost))}")

    return problem


transition_coeffs = [5, 3, 6, 2, 3, 4, 5, 6, 7, 5, 6, 4, 4, 8, 5, 3]
needs = [400, 800, 200, 800]

print("===============================================================================================")
print("Варіант №1. Розширюємо потужність першого заводу із додатковими витратами на одиницю продукції")
print("===============================================================================================")

production_coeffs1 = [12, 3, 6, 0]
powers1 = [900, 700, 600, 0]
production_cost1 = sum([c * n for c, n in zip(production_coeffs1, powers1)])
vars1 = solve_phase_one(4, 4, transition_coeffs, needs, powers1)
print(f"Витрати на виробництво:     {int(value(production_cost1))}")
print(f"Загальні витрати:           {int(value(vars1.objective) + int(value(production_cost1)))}")

print("===============================================================================================")
print("Варіант №2. Розширюємо потужність другого заводу із додатковими витратами на одиницю продукції")
print("===============================================================================================")

production_coeffs2 = [9, 5, 6, 0]
powers2 = [500, 1100, 600, 0]
production_cost2 = sum([c * n for c, n in zip(production_coeffs2, powers2)])
vars2 = solve_phase_one(4, 4, transition_coeffs, needs, powers2)
print(f"Витрати на виробництво:     {int(value(production_cost2))}")
print(f"Загальні витрати:           {int(value(vars2.objective) + int(value(production_cost2)))}")

print("===============================================================================================")
print("Варіант №3. Розширюємо потужність третього заводу із додатковими витратами на одиницю продукції")
print("===============================================================================================")

production_coeffs3 = [9, 3, 11, 0]
powers3 = [500, 700, 1000, 0]
production_cost3 = sum([c * n for c, n in zip(production_coeffs3, powers3)])
vars3 = solve_phase_one(4, 4, transition_coeffs, needs, powers3)
print(f"Витрати на виробництво:     {int(value(production_cost3))}")
print(f"Загальні витрати:           {int(value(vars3.objective) + int(value(production_cost3)))}")

print("===============================================================================================")
print("Варіант №4. Будуємо четвертий завод без додаткових витрат на одиницю продукції")
print("===============================================================================================")

production_coeffs4 = [9, 3, 6, 10]
powers4 = [500, 700, 600, 400]
production_cost4 = sum([c * n for c, n in zip(production_coeffs4, powers4)])
vars4 = solve_phase_one(4, 4, transition_coeffs, needs, powers4)
print(f"Витрати на виробництво:     {int(value(production_cost4))}")
print(f"Загальні витрати:           {int(value(vars4.objective) + int(value(production_cost4)))}")

print()
print("==================================================================================================")
print("Вихідна задача з нечіткими обмеженнями")
print("==================================================================================================")
print("+-------------+------------------------------------+------------+-----------+---------+----------+\n"
      "|             | Завод 1  Завод 2  Завод 3  Завод 4 |  Попит,min | Попит,max | Дефіцит | Надлишок |\n"
      "+-------------+------------------------------------+------------+-----------+---------+----------+\n"
      "| Витрати     |    9        3        6       10    |                                             |\n"
      "+-------------+------------------------------------+------------+-----------+---------+----------+\n"
      "| Споживач 1  |    5        3        6        2    |     300    |    500    |    5    |     8    |\n"
      "| Споживач 2  |    3        4        5        6    |     700    |   1100    |    6    |    10    |\n"
      "| Споживач 3  |    7        5        6        4    |     200    |    400    |    6    |    19    |\n"
      "| Споживач 4  |    4        8        5        3    |     600    |   1000    |    3    |     6    |\n"
      "+-------------+------------------------------------+------------+-----------+---------+----------+\n"
      "| Потужність  |   500      700      600      ---   |                                             |\n"
      "| Дод.витрати |    3        2        5       ---   |                                             |\n"
      "+-------------+------------------------------------+------------+-----------+---------+----------+")


def solve_phase_two(m: int, n: int, C: list, X: list, B_min, B_max, A: list):
    Y = [LpVariable(f"Y{i+1}{j+1}", lowBound=0) for i in range(m) for j in range(n)]
    # for idx, x in enumerate(X):
    #     Y[idx].setInitialValue(value(x))
    transition_cost = sum([c * (y - x) for c, y, x in zip(C, Y, X)])
    problem = pulp.LpProblem("0", LpMinimize)
    problem += transition_cost, "Цільова функція"

    # Обмеження за попитом
    # for idx, (b_min, b_max) in enumerate(zip(B_min, B_max)):
    #     problem += sum(Y[n * idx:n * (idx + 1)]) >= b_min, f"B{idx + 1}1"
    #     problem += sum(Y[n * idx:n * (idx + 1)]) <= b_max, f"B{idx + 1}2"

    # Обмеження за потужністю
    for idx, a in enumerate(A):
        problem += sum(Y[idx::m]) == a, f"A{idx + 1}1"

    problem += sum(Y) == sum(X), f"total"
    problem.solve()

    return problem


def calc_cost(m, n, X, C, B_min, B_max, S, Q):
    trans_cost = value(sum([c * x for c, x in zip(C, X)]))

    extra_cost = 0
    for j in range(n):
        b = (B_min[j] + B_max[j]) / 2
        w = value(sum(X[n*j:n*j+m]))

        q = Q[j]
        s = S[j]
        b_min = B_min[j]
        b_max = B_max[j]
        extra_cost += q * (b - w) + 0.5 * (s + q) * (w - b_min) ** 2 / (b_max - b_min)

    return trans_cost, extra_cost


def gradients(m, n, C, X, B_min, B_max, S, Q):
    grads = []

    for i in range(m):
        for j in range(n):
            c = C[i*n+j]
            q = Q[j]
            s = S[j]
            b_min = B_min[j]
            b_max = B_max[j]
            # print(c, q, s, b_min, b_max)

            w = sum(X[n*j:n*j+m])

            grad = c - q + (s + q) * (w - b_min) / (b_max - b_min)
            grads.append(grad)
    print(grads)
    return grads


def calc_alpha(m, n, C, X, Y, B_min, B_max, S, Q):
    lambda1 = 0
    lambda2 = 0
    for c, x, y in zip(C, X, Y):
        lambda1 += c * (y - x)

    for j in range(n):
        s = S[j]
        q = Q[j]
        b_min = B_min[j]
        b_max = B_max[j]

        X_j = X[n * j:n * j + m]
        Y_j = Y[n * j:n * j + m]
        coeff = 0.5 * (s + q) / (b_max - b_min)

        diff = sum([y - x for x, y in zip(X_j, Y_j)])

        lambda1 += coeff * 2 * diff * (sum(X_j) - b_min) - q * diff
        lambda2 += coeff * diff ** 2

    if lambda2 == 0:
        return 0

    return -0.5 * lambda1 / lambda2


def diff(X, Y):
    return math.sqrt(sum([(value(y) - value(x))**2 for x, y in zip(X, Y)]))


def solve_with_gradients(m, n, X, C, A, B_min, B_max, S, Q):
    X_hist = []
    F_hist = []
    X = [value(x) for x in X]
    cost = calc_cost(m, n, X, C, B_min, B_max, S, Q)
    print('initial vars:', X)
    print('initial cost:', cost)
    i = 0
    for i in range(10):
        X_hist.append([x for x in X])
        F_hist.append(cost)
        i += 1
        grads = gradients(m, n, C, X, B_min, B_max, S, Q)
        prob = solve_phase_two(m, n, grads, X, B_min, B_max, A)
        new_X = [value(x) for x in prob.variables()]
        print(new_X)
        l = max(-1, min(1, calc_alpha(m, n, C, X, new_X, B_min, B_max, S, Q)))

        if abs(l) < 0.0001:
            break

        X = [x + round(l*(value(new_x) - x)) for new_x, x in zip(new_X, X)]
        cost = calc_cost(m, n, X, C, B_min, B_max, S, Q)
        print('iter', i, 'vars:', X)
        print('iter', i, 'cost:', cost)

    print("END")
    print([sum(X[i*n:i*n+m]) for i in range(m)])
    for x, f in zip(X_hist, F_hist):
        print(x, f, sum(f))
    return X_hist, F_hist


C = [5, 3, 6, 2, 3, 4, 5, 6, 7, 5, 6, 4, 4, 8, 5, 3]
C2 = [9, 5, 6, 0]
C2 = [0, 2, 0, 0]
C = [c+c2 for c, c2 in zip(C, itertools.cycle(C2))]

X = vars2.variables()
A = [500, 1100, 600, 0]
B_min = [300, 700, 200, 600]
B_max = [500, 1100, 400, 1000]
Q = [5, 6, 600, 3]
S = [8, 10, 19, 6]

solve_with_gradients(4, 4, X, C, A, B_min, B_max, S, Q)
