import numpy as np
from scipy.optimize import minimize

m = 4
n = 4
C = [5, 3, 6, 2, 3, 4, 5, 6, 7, 5, 6, 4, 4, 8, 5, 3]
LB = [300, 700, 200, 600]
UB = [500, 1000, 400, 1000]
R = [40, 50, 95, 30]
S = [25, 30, 30, 15]
bounds = [(0, np.inf) for _ in range(m * n)]


def objective(x):
    sum_eq = 0

    for c_ij, x_ij in zip(C, x):
        sum_eq += c_ij * x_ij

    for x_j, lb_j, ub_j, r_j, s_j in zip(x.reshape((m, n)).T, LB, UB, R, S):
        sum_eq += r_j * (0.5 * (lb_j + ub_j) - sum(x_j))
        sum_eq += 0.5 * (sum(x_j) - lb_j) * (sum(x_j) - lb_j) * (s_j + r_j) / (ub_j - lb_j)

    return sum_eq


cons1 = {"type": "eq", "fun": lambda x: 500 - x[0] - x[4] - x[8] - x[12]}
cons2 = {"type": "eq", "fun": lambda x: 700 - x[1] - x[5] - x[9] - x[13]}
cons3 = {"type": "eq", "fun": lambda x: 600 - x[2] - x[6] - x[10] - x[14]}
cons4 = {"type": "eq", "fun": lambda x: 400 - x[3] - x[7] - x[11] - x[15]}
int_cons = [{"type": "ineq", "fun": lambda x: -x[ij]+int(x[ij])} for ij in range(16)]
cons = [cons1, cons2, cons3, cons4] + int_cons

# initial guesses
x0 = np.zeros(m*n)

# show initial objective
print('Initial SSE Objective: ' + str(objective(x0)))

solution = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=cons, tol=10e-16)
x = solution.x

# show final objective
print('Final SSE Objective: ' + str(objective(x)))
print(sum(x))
# print solution
print('Solution')
x_res = x.reshape(m, n)

for j, x_j in enumerate(x_res):
    for i, x_ij in enumerate(x_j):
        print(f"x{i}{j} = {str(x_ij)}")
