from pulp import *

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
      "| Споживач 3  |    7        5        6        4    |  400  |\n"
      "| Споживач 4  |    4        8        5        3    |  200  |\n"
      "+-------------+------------------------------------+-------+\n"
      "| Потужність  |   500      700      600      ---   |       |\n"
      "| Дод.витрати |    3        2        5       ---   |       |\n"
      "+-------------+------------------------------------+-------+\n")


def solve_simple(consumers: int, producers: int,
                 transition_coeffs: list, production_coeffs: list,
                 needs: list, powers: list):
    errors = []

    if len(transition_coeffs) != consumers * producers:
        errors.append("Транспортні витрати вказані невірно")

    if len(production_coeffs) != producers:
        errors.append("Витрати на виробництво вказані невірно")

    if len(needs) != consumers:
        errors.append("Попит споживачів вказан невірно")

    if len(powers) != producers:
        errors.append("Потужність заводів вказана невірно")

    if sum(needs) > sum(powers):
        errors.append("Попиту споживачів перевищує потужність заводів")

    if errors:
        return errors

    X = []
    for i in range(consumers):
        for j in range(producers):
            X.append(pulp.LpVariable(f"X{i+1}{j+1}", lowBound=0, cat=pulp.LpInteger))

    transition_cost = sum([c_ij*x_ij for c_ij, x_ij in zip(transition_coeffs, X)])
    production_cost = sum([c * n for c, n in zip(production_coeffs, powers)])

    problem = pulp.LpProblem("0", LpMinimize)
    problem += transition_cost, "Цільова функція"

    print("Цільова функція:", transition_cost)

    print("Обмеження за попитом:")
    # Обмеження за попитом
    for idx, need in enumerate(needs):
        print(sum(X[producers*idx:producers*(idx+1)]) == need)
        problem += sum(X[producers*idx:producers*(idx+1)]) == need, f"споживач {idx + 1}"

    print("Обмеження за потужністю:")
    for idx, power in enumerate(powers):
        print(sum(X[idx::consumers]) <= power)
        problem += sum(X[idx::consumers]) <= power, f"завод {idx + 1}"

    problem.solve()

    print("План поставки:")
    for variable in problem.variables():
        if variable.varValue > 0:
            var_name = variable.name
            print(f"Завод {var_name[2]} -> Споживач {var_name[1]}: {int(variable.varValue)}")

    print(f"Витрати на транспортування: {int(value(transition_cost))}")
    print(f"Витрати на виробництво:     {int(value(production_cost))}")
    print(f"Загальні витрати:           {int(value(transition_cost+production_cost))}")

    return problem


transition_coeffs = [5, 3, 6, 2, 3, 4, 5, 6, 7, 5, 6, 4, 4, 8, 5, 3]
needs = [400, 800, 400, 200]

print("===============================================================================================")
print("Варіант №1. Розширюємо потужність першого заводу із додатковими витратами на одиницю продукції")
print("===============================================================================================")

production_coeffs1 = [12, 3, 6, 0]
powers1 = [900, 700, 600, 0]
vars1 = solve_simple(4, 4, transition_coeffs, production_coeffs1, needs, powers1)

print("===============================================================================================")
print("Варіант №2. Розширюємо потужність другого заводу із додатковими витратами на одиницю продукції")
print("===============================================================================================")

production_coeffs2 = [9, 5, 6, 0]
powers2 = [500, 1100, 600, 0]
vars2 = solve_simple(4, 4, transition_coeffs, production_coeffs2, needs, powers2)

print("===============================================================================================")
print("Варіант №3. Розширюємо потужність третього заводу із додатковими витратами на одиницю продукції")
print("===============================================================================================")

production_coeffs3 = [9, 3, 11, 0]
powers3 = [500, 700, 1000, 0]
vars3 = solve_simple(4, 4, transition_coeffs, production_coeffs3, needs, powers3)

print("===============================================================================================")
print("Варіант №4. Будуємо четвертий завод без додаткових витрат на одиницю продукції")
print("===============================================================================================")

production_coeffs4 = [9, 3, 6, 10]
powers4 = [500, 700, 600, 400]
vars4 = solve_simple(4, 4, transition_coeffs, production_coeffs4, needs, powers4)

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

X = []
for i in range(4):
    for j in range(4):
        X.append(pulp.LpVariable(f"X{i + 1}{j + 1}", lowBound=0, cat=pulp.LpInteger))

r = [5, 6, 6, 3]
s = [8, 10, 19, 6]


problem_final = LpProblem('0', LpMinimize)
q = [6, 7, 8, 11]
b = [400, 900, 300, 800]

consumers = [X[idx*4:(idx+1)*4] for idx in range(4)]
cost_q = sum([q_j * (b_j - sum(X_j)) for q_j, b_j, X_j in zip(q, b, consumers)])
print(cost_q)
