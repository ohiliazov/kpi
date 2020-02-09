from itertools import cycle
from pulp import *

# Споживач №1
x11 = pulp.LpVariable("x11", lowBound=0, cat=LpInteger)
x12 = pulp.LpVariable("x12", lowBound=0, cat=LpInteger)
x13 = pulp.LpVariable("x13", lowBound=0, cat=LpInteger)
x14 = pulp.LpVariable("x14", lowBound=0, cat=LpInteger)

# Споживач №2
x21 = pulp.LpVariable("x21", lowBound=0, cat=LpInteger)
x22 = pulp.LpVariable("x22", lowBound=0, cat=LpInteger)
x23 = pulp.LpVariable("x23", lowBound=0, cat=LpInteger)
x24 = pulp.LpVariable("x24", lowBound=0, cat=LpInteger)

# Споживач №3
x31 = pulp.LpVariable("x31", lowBound=0, cat=LpInteger)
x32 = pulp.LpVariable("x32", lowBound=0, cat=LpInteger)
x33 = pulp.LpVariable("x33", lowBound=0, cat=LpInteger)
x34 = pulp.LpVariable("x34", lowBound=0, cat=LpInteger)

# Споживач №4
x41 = pulp.LpVariable("x41", lowBound=0, cat=LpInteger)
x42 = pulp.LpVariable("x42", lowBound=0, cat=LpInteger)
x43 = pulp.LpVariable("x43", lowBound=0, cat=LpInteger)
x44 = pulp.LpVariable("x44", lowBound=0, cat=LpInteger)

# Споживачі
consumers = [
    [x11, x12, x13, x14],
    [x21, x22, x23, x24],
    [x31, x32, x33, x34],
    [x41, x42, x43, x44],
]
consumer_1 = [x11, x12, x13, x14]
consumer_2 = [x21, x22, x23, x24]
consumer_3 = [x31, x32, x33, x34]
consumer_4 = [x41, x42, x43, x44]

# Заводи
producers = [
    [x11, x21, x31, x41],
    [x12, x22, x32, x42],
    [x13, x23, x33, x43],
    [x14, x24, x34, x44],
]
factory_1 = [x11, x21, x31, x41]
factory_2 = [x12, x22, x32, x42]
factory_3 = [x13, x23, x33, x43]
factory_4 = [x14, x24, x34, x44]

print("============================================================")
print("Вихідна задача з чіткими умовами")
print("============================================================")
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
C = [
    [5, 3, 6, 2],
    [3, 4, 5, 6],
    [7, 5, 6, 4],
    [4, 8, 5, 3],
]
prod_C = [9, 3, 6, 10]
needs = [400, 800, 400, 200]
transition_cost = sum([c_ij * x_ij for c_j, x_j in zip(C, consumers) for c_ij, x_ij in zip(c_j, x_j)])
production_cost = sum([prod_c_i * sum(producer) for prod_c_i, producer in zip(prod_C, producers)])
base_cost = transition_cost + production_cost

print()
print("==============================================================================================")
print("Варіант №1. Розширюємо потужність першого заводу із додатковими витратами на одиницю продукції")
print("==============================================================================================")

# Додаткові витрати на виробництво одиниці продукції на першому заводі
powers = [900, 700, 600, 0]

extra_cost = 3 * sum(producers[0])
total_cost = base_cost + extra_cost
print(total_cost)
problem1 = pulp.LpProblem("0", LpMinimize)
problem1 += total_cost, "Цільова функція"

# Обмеження за попитом
for idx, consumer, need in zip(range(4), consumers, needs):
    problem1 += sum(consumer) == need, str(f"Споживач {idx+1}")

# Обмеження за потужністю
for idx, producer, power in zip(range(4), producers, powers):
    problem1 += sum(producer) <= power, str(f"Завод {idx+1}")

print(problem1)
problem1.solve()
print("План поставки:")

for variable in problem1.variables():
    if variable.varValue > 0:
        var_name = variable.name
        print(f"Завод {var_name[1]} -> Споживач {var_name[2]}: {int(variable.varValue)}")


print(transition_cost)
print(f"Витрати на транспортування: {int(value(transition_cost))}")
print(production_cost)
print(f"Витрати на виробництво:     {int(value(production_cost))}")
print(extra_cost)
print(f"Додаткові витрати:          {int(value(extra_cost))}")
print(value(sum(producers[0])), value(sum(producers[1])), value(sum(producers[2])), value(sum(producers[3])))
print(f"Загальні витрати:           {int(value(total_cost))}")
print()
print("==============================================================================================")
print("Варіант №2. Розширюємо потужність другого заводу із додатковими витратами на одиницю продукції")
print("==============================================================================================")

# Додаткові витрати на виробництво одиниці продукції на першому заводі
powers = [500, 1100, 600, 0]

extra_cost = 2 * sum(producers[1])
total_cost = base_cost + extra_cost

problem2 = pulp.LpProblem("0", LpMinimize)
problem2 += total_cost, "Цільова функція"

# Обмеження за попитом
for idx, consumer, need in zip(range(4), consumers, needs):
    problem2 += sum(consumer) == need, str(f"Споживач {idx+1}")

# Обмеження за потужністю
for idx, producer, power in zip(range(4), producers, powers):
    problem2 += sum(producer) <= power, str(f"Завод {idx+1}")

problem2.solve()
print("План поставки:")

for variable in problem2.variables():
    if variable.varValue > 0:
        var_name = variable.name
        print(f"Завод {var_name[1]} -> Споживач {var_name[2]}: {int(variable.varValue)}")

print(f"Витрати на транспортування: {int(value(transition_cost))}")
print(f"Витрати на виробництво:     {int(value(production_cost))}")
print(f"Додаткові витрати:          {int(value(extra_cost))}")
print(f"Загальні витрати:           {int(value(total_cost))}")
print()
print("===============================================================================================")
print("Варіант №3. Розширюємо потужність третього заводу із додатковими витратами на одиницю продукції")
print("===============================================================================================")

# Додаткові витрати на виробництво одиниці продукції на першому заводі
powers = [500, 700, 1000, 0]

extra_cost = 5 * sum(producers[2])
total_cost = base_cost + extra_cost

problem3 = pulp.LpProblem("0", LpMinimize)
problem3 += total_cost, "Цільова функція"

# Обмеження за попитом
for idx, consumer, need in zip(range(4), consumers, needs):
    problem3 += sum(consumer) == need, str(f"Споживач {idx+1}")

# Обмеження за потужністю
for idx, producer, power in zip(range(4), producers, powers):
    problem3 += sum(producer) <= power, str(f"Завод {idx+1}")

problem3.solve()
print("План поставки:")

for variable in problem3.variables():
    if variable.varValue > 0:
        var_name = variable.name
        print(f"Завод {var_name[1]} -> Споживач {var_name[2]}: {int(variable.varValue)}")

print(f"Витрати на транспортування: {int(value(transition_cost))}")
print(f"Витрати на виробництво:     {int(value(production_cost))}")
print(f"Додаткові витрати:          {int(value(extra_cost))}")
print(f"Загальні витрати:           {int(value(total_cost))}")
print()
print("==============================================================================")
print("Варіант №4. Будуємо четвертий завод без додаткових витрат на одиницю продукції")
print("==============================================================================")

# Додаткові витрати на виробництво одиниці продукції на першому заводі
powers = [500, 700, 600, 400]

problem4 = pulp.LpProblem("0", LpMinimize)
problem4 += base_cost, "Цільова функція"


# Обмеження за попитом
for idx, consumer, need in zip(range(4), consumers, needs):
    problem4 += sum(consumer) == need, str(f"Споживач {idx+1}")

# Обмеження за потужністю
for idx, producer, power in zip(range(4), producers, powers):
    problem4 += sum(producer) <= power, str(f"Завод {idx+1}")

problem4.solve()
print("План поставки:")

for variable in problem4.variables():
    if variable.varValue > 0:
        var_name = variable.name
        print(f"Завод {var_name[1]} -> Споживач {var_name[2]}: {int(variable.varValue)}")

print(f"Витрати на транспортування: {int(value(transition_cost))}")
print(f"Витрати на виробництво:     {int(value(production_cost))}")
print(f"Загальні витрати:           {int(value(total_cost))}")
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
r = [5, 6, 6, 3]
s = [8, 10, 19, 6]


problem_final = LpProblem('0', LpMinimize)
q = [6, 7, 8, 11]
b = [400, 900, 300, 800]
consumers = [consumer_1, consumer_2, consumer_3, consumer_4]
print(transition_cost)
cost_q = sum([q_j * (b_j - sum(X_j)) for q_j, b_j, X_j in zip(q, b, consumers)])
