import cvxpy as cp
import numpy as np


class TransportProblem:
    def __init__(
        self,
        sources: int,
        targets: int,
        capacity: np.ndarray,
        prod_cost: np.ndarray,
        trans_cost: np.ndarray,
    ):
        assert isinstance(sources, int) and sources > 0
        assert isinstance(targets, int) and targets > 0
        assert capacity.shape == (sources,)
        assert prod_cost.shape == (sources,)
        assert trans_cost.shape == (targets, sources)
        self.sources = sources
        self.targets = targets
        self.capacity = capacity
        self.prod_cost = prod_cost
        self.trans_cost = trans_cost
        self.x = cp.Variable((m, n), integer=True)
        self.prob = None

    @property
    def cost(self):
        return self.trans_cost + self.prod_cost

    @property
    def prod_expr(self):
        return cp.sum(cp.multiply(self.prod_cost, cp.sum(self.x, axis=0)))

    @property
    def prod_value(self):
        return self.prod_expr.value

    @property
    def trans_expr(self):
        return cp.sum(cp.multiply(self.trans_cost, self.x))

    @property
    def trans_value(self):
        return self.trans_expr.value

    @property
    def expr(self):
        raise NotImplementedError

    @property
    def constraints(self):
        raise NotImplementedError

    @property
    def total_value(self):
        return self.expr.value

    def solve(self, solver=cp.CPLEX, verbose=False):
        self.prob = cp.Problem(cp.Minimize(self.expr), self.constraints)
        self.prob.solve(solver=solver, verbose=verbose)


class LinearTransportProblem(TransportProblem):
    def __init__(
        self,
        sources: int,
        targets: int,
        capacity: np.ndarray,
        demand: np.ndarray,
        prod_cost: np.ndarray,
        trans_cost: np.ndarray,
    ):
        super().__init__(sources, targets, capacity, prod_cost, trans_cost)
        assert demand.shape == (targets,)
        self.demand = demand

    @property
    def expr(self):
        return self.trans_expr + self.prod_expr

    @property
    def constraints(self):
        return [
            self.x >= 0,
            cp.sum(self.x, axis=0) == self.capacity,
            cp.sum(self.x, axis=1) == self.demand,
        ]

    def print(self):
        print(
            f"Linear result: "
            f"total = {self.total_value:.2f} "
            f"production = {self.prod_value:.2f}, "
            f"transport = {self.trans_value:.2f}"
        )
        print(f"Optimal routes: \n{self.x.value.astype(int)}")


class NonlinearTransportProblem(TransportProblem):
    def __init__(
        self,
        sources: int,
        targets: int,
        capacity: np.ndarray,
        prod_cost: np.ndarray,
        trans_cost: np.ndarray,
        lower_demand: np.ndarray,
        upper_demand: np.ndarray,
        shortage: np.ndarray,
        overflow: np.ndarray,
        init_value: np.ndarray,
    ):
        super().__init__(sources, targets, capacity, prod_cost, trans_cost)
        assert lower_demand.shape == (targets,)
        assert upper_demand.shape == (targets,)
        assert shortage.shape == (targets,)
        assert overflow.shape == (targets,)
        self.lower_demand = lower_demand
        self.upper_demand = upper_demand
        self.demand = (lower_demand + upper_demand) / 2
        self.shortage = shortage
        self.overflow = overflow
        self.x = cp.Variable((n, m), integer=True, value=init_value)

    @property
    def penalty_expr(self):
        penalty_const = (
            (self.overflow + self.shortage)
            / (self.upper_demand - self.lower_demand)
            / 2
        )
        expr0 = cp.multiply(self.shortage, self.demand - cp.sum(self.x, axis=1))
        expr1 = cp.square(cp.sum(self.x, axis=1) - self.lower_demand)
        return cp.sum(expr0 + cp.multiply(expr1, penalty_const))

    @property
    def penalty_value(self):
        return self.penalty_expr.value

    @property
    def expr(self):
        return self.trans_expr + self.prod_expr + self.penalty_expr

    @property
    def constraints(self):
        return [
            self.x >= 0,
            cp.sum(self.x, axis=0) == self.capacity,
        ]

    def print(self):
        print(
            f"Nonlinear result: "
            f"total = {self.total_value:.2f}, "
            f"production = {self.prod_value:.2f}, "
            f"transport = {self.trans_value:.2f}, "
            f"penalty = {self.penalty_value:.2f}"
        )
        print(f"Optimal routes: \n{self.x.value.astype(int)}")
        print(
            f"Optimal demand satisfaction: {np.sum(self.x.value, axis=1).astype(int)}\n"
        )


def solve(m, n, a, b, p, c, lb, ub, r, s, verbose: bool, to_print: bool):
    linear_solver = LinearTransportProblem(m, n, a, b, p, c)
    linear_solver.solve(verbose=verbose)

    if to_print:
        linear_solver.print()
    x = linear_solver.x.value.astype(int)
    nonlinear_solver = NonlinearTransportProblem(m, n, a, p, c, lb, ub, r, s, x)
    nonlinear_solver.solve(verbose=verbose)

    if to_print:
        nonlinear_solver.print()
        print(nonlinear_solver.x.value - linear_solver.x.value)

    return linear_solver.total_value, nonlinear_solver.total_value


m, n = 4, 4

b = np.array([400, 800, 200, 800])
c = np.array([[5, 3, 6, 2], [3, 4, 5, 6], [7, 5, 6, 4], [4, 8, 5, 3],])
lb = np.array([300, 700, 200, 600])
ub = np.array([500, 1000, 400, 1000])
r = np.array([8, 10, 19, 6]) * 3
s = np.array([5, 6, 6, 3]) * 3

a_list = np.array(
    [[900, 700, 600, 0], [500, 1100, 600, 0], [500, 700, 1000, 0], [500, 700, 600, 400]]
)
p_list = np.array([[12, 3, 6, 10], [9, 5, 6, 10], [9, 3, 11, 10], [9, 3, 6, 10]])


linear_values = []
nonlinear_values = []
for a, p in zip(a_list, p_list):
    linear_value, nonlinear_value = solve(
        m, n, a, b, p, c, lb, ub, r, s, verbose=True, to_print=True
    )
    linear_values.append(linear_value)
    nonlinear_values.append(nonlinear_value)

linear_values = np.array(linear_values)
nonlinear_values = np.array(nonlinear_values)
print(nonlinear_values)

print("Performing sensitivity check by transportation cost...")
sensitivity_max = []
sensitivity_upper = []
sensitivity_lower = []

for idx, row in enumerate(np.eye(m * n).reshape(m * n, m, n)):
    values_max = []
    values_upper = []
    values_lower = []

    for a, p in zip(a_list, p_list):
        c_row = c.copy()
        c_row[row == 1] = 10000
        max_linear, max_nonlinear = solve(
            m, n, a, b, p, c_row, lb, ub, r, s, verbose=False, to_print=False
        )
        upper_linear, upper_nonlinear = solve(
            m, n, a, b, p, c - row, lb, ub, r, s, verbose=False, to_print=False
        )
        lower_linear, lower_nonlinear = solve(
            m, n, a, b, p, c + row, lb, ub, r, s, verbose=False, to_print=False
        )

        values_max.append(max_nonlinear)
        values_upper.append(upper_nonlinear)
        values_lower.append(lower_nonlinear)

    sensitivity_max.append(np.array(values_max) - nonlinear_values)
    sensitivity_upper.append(np.array(values_upper) - nonlinear_values)
    sensitivity_lower.append(np.array(values_lower) - nonlinear_values)


sensitivity_max = np.array(sensitivity_max).T.reshape(4, m, n)
print("\nRemoved route (increased each cost to 10000):")
print(sensitivity_max)
print(np.average(sensitivity_max, axis=(1, 2)))

sensitivity_upper = np.array(sensitivity_upper).T.reshape(4, m, n)
print("\nRemoved route (increased each cost by 1):")
print(sensitivity_upper)
print(np.average(sensitivity_upper, axis=(1, 2)))

sensitivity_lower = np.array(sensitivity_lower).T.reshape(4, m, n)
print("\nRemoved route (decreased each cost by 1):")
print(sensitivity_lower)
print(np.average(sensitivity_lower, axis=(1, 2)))

print("Performing sensitivity check...")
r_sensitivity_upper = []
r_sensitivity_lower = []
s_sensitivity_upper = []
s_sensitivity_lower = []

for idx, row in enumerate(np.eye(m)):
    r_values_upper = []
    r_values_lower = []
    s_values_upper = []
    s_values_lower = []

    for a, p in zip(a_list, p_list):
        r_upper_linear, r_upper_nonlinear = solve(
            m, n, a, b, p, c, lb, ub, r + row, s, verbose=False, to_print=False
        )
        r_lower_linear, r_lower_nonlinear = solve(
            m, n, a, b, p, c, lb, ub, r - row, s, verbose=False, to_print=False
        )
        s_upper_linear, s_upper_nonlinear = solve(
            m, n, a, b, p, c, lb, ub, r, s + row, verbose=False, to_print=False
        )
        s_lower_linear, s_lower_nonlinear = solve(
            m, n, a, b, p, c, lb, ub, r, s - row, verbose=False, to_print=False
        )

        r_values_upper.append(r_upper_nonlinear)
        r_values_lower.append(r_lower_nonlinear)
        s_values_upper.append(s_upper_nonlinear)
        s_values_lower.append(s_lower_nonlinear)

    r_sensitivity_upper.append(np.array(r_values_upper) - nonlinear_values)
    r_sensitivity_lower.append(np.array(r_values_lower) - nonlinear_values)
    s_sensitivity_upper.append(np.array(s_values_upper) - nonlinear_values)
    s_sensitivity_lower.append(np.array(s_values_lower) - nonlinear_values)


r_sensitivity_upper = np.array(r_sensitivity_upper).T
print("\nIncreased each deficit penalty by 1:")
print(r_sensitivity_upper)

r_sensitivity_lower = np.array(r_sensitivity_lower).T
print("\nDecreased each deficit penalty by 1:")
print(r_sensitivity_lower)

s_sensitivity_upper = np.array(s_sensitivity_upper).T
print("\nIncreased each overflow penalty by 1:")
print(s_sensitivity_upper)

s_sensitivity_lower = np.array(s_sensitivity_lower).T
print("\nDecreased each overflow penalty by 1:")
print(s_sensitivity_lower)
