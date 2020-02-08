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
consumer_1 = [x11, x12, x13, x14]
consumer_2 = [x21, x22, x23, x24]
consumer_3 = [x31, x32, x33, x34]
consumer_4 = [x41, x42, x43, x44]

# Заводи
factory_1 = [x11, x21, x31, x41]
factory_2 = [x12, x22, x32, x42]
factory_3 = [x13, x23, x33, x43]
factory_4 = [x14, x24, x34, x44]

# Вихідна задача
# +-------------+------------------------------------+-------+
# |             | Завод 1  Завод 2  Завод 3  Завод 4 | Попит |
# +-------------+------------------------------------+-------+
# | Споживач 1  |    5        3        6        2    |  400  |
# | Споживач 2  |    3        4        5        6    |  800  |
# | Споживач 3  |    7        5        6        4    |  400  |
# | Споживач 4  |    4        8        5        3    |  200  |
# +-------------+------------------------------------+-------+
# | Витрати     |    9        3        6        0    |       |
# | Потужність  |   500      700      600       0    |       |
# +-------------+------------------------------------+-------+


all_vars = [x11, x12, x13, x14, x21, x22, x23, x24, x31, x32, x33, x34, x41, x42, x43, x44]
transition_coeffs = [5, 3, 6, 2, 3, 4, 5, 6, 7, 5, 6, 4, 4, 8, 5, 3]
production_coeffs = [9, 3, 6, 0, 9, 3, 6, 0, 9, 3, 6, 0, 9, 3, 6, 0]
coefficients = list([tc + pc for tc, pc in zip(transition_coeffs, production_coeffs)])
transition_cost = sum([c * x for c, x in zip(transition_coeffs, all_vars)])

print("Транспортні витрати:", transition_cost)
print()
print("Варіант №1. Розширюємо потужність першого заводу із додатковими витратами на одиницю продукції")

# Додаткові витрати на виробництво одиниці продукції на першому заводі
production_coeffs = [12, 3, 6, 0, 12, 3, 6, 0, 12, 3, 6, 0, 12, 3, 6, 0]
production_cost = sum([c * x for c, x in zip(production_coeffs, all_vars)])
print("Витрати на виробництво:", production_cost)
total_cost = transition_cost + production_cost
print("Цільова функція:", total_cost)

problem = pulp.LpProblem("0", LpMinimize)
problem += total_cost, "Цільова функція"

# Обмеження за попитом
problem += sum(consumer_1) == 400, "1"
problem += sum(consumer_2) == 800, "2"
problem += sum(consumer_3) == 200, "3"
problem += sum(consumer_4) == 800, "4"

# Обмеження за потужністю
problem += sum(factory_1) <= 900, "5"  # 500 -> 900
problem += sum(factory_2) <= 700, "6"
problem += sum(factory_3) <= 600, "7"
problem += sum(factory_4) == 0, "8"

problem.solve()
print("Результат:")

for variable in problem.variables():
    if variable.varValue > 0:
        print(variable.name, "=", int(variable.varValue))

print("Стоимость доставки:")
print(int(value(problem.objective)))
