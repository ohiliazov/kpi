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
        assert capacity.shape == (sources, )
        assert prod_cost.shape == (sources, )
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
    def prod_value(self):
        return np.sum(np.multiply(self.prod_cost, self.x.value))

    @property
    def trans_value(self):
        return np.sum(np.multiply(self.trans_cost, self.x.value))

    @property
    def expr(self):
        raise NotImplementedError

    @property
    def constraints(self):
        raise NotImplementedError

    def solve(self, verbose=False):
        self.prob = cp.Problem(cp.Minimize(self.expr), self.constraints)
        self.prob.solve(solver=cp.CPLEX, verbose=verbose)


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
        assert demand.shape == (targets, )
        self.demand = demand

    @property
    def expr(self):
        return cp.sum(cp.multiply(self.trans_cost, self.x))

    @property
    def total_value(self):
        return self.trans_value + self.prod_value

    @property
    def constraints(self):
        return [
            cp.sum(self.x, axis=0) <= self.capacity,
            cp.sum(self.x, axis=1) >= self.demand,
            self.x >= 0,
        ]

    def print(self):
        print(f"Linear result: "
              f"total = {self.total_value:.2f} "
              f"production = {self.prod_value:.2f}, "
              f"transport = {self.trans_value:.2f}")
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
    ):
        super().__init__(sources, targets, capacity, prod_cost, trans_cost)
        assert lower_demand.shape == (targets, )
        assert upper_demand.shape == (targets, )
        assert shortage.shape == (targets, )
        assert overflow.shape == (targets, )
        self.lower_demand = lower_demand
        self.upper_demand = upper_demand
        self.demand = (lower_demand + upper_demand) / 2
        self.shortage = shortage
        self.overflow = overflow

    @property
    def penalty_const(self):
        return (self.overflow + self.shortage) / (self.upper_demand - self.lower_demand) / 2

    @property
    def penalty_expr(self):
        expr0 = cp.multiply(self.shortage, self.demand - cp.sum(self.x, axis=1))
        expr1 = cp.square(cp.sum(self.x, axis=1) - self.lower_demand)
        return cp.sum(expr0 + cp.multiply(expr1, self.penalty_const))

    @property
    def expr(self):
        return cp.sum(cp.multiply(self.trans_cost, self.x)) + self.penalty_expr

    @property
    def penalty_value(self):
        return self.penalty_expr.value

    @property
    def total_value(self):
        return self.trans_value + self.prod_value + self.penalty_value

    @property
    def constraints(self):
        return [
            cp.sum(self.x, axis=0) <= self.capacity,
            self.x >= 0,
        ]

    def print(self):
        print(f"Nonlinear result: "
              f"total = {self.total_value:.2f}, "
              f"production = {self.prod_value:.2f}, "
              f"transport = {self.trans_value:.2f}, "
              f"penalty = {self.penalty_value:.2f}")
        print(f"Optimal routes: \n{self.x.value.astype(int)}\n")


m, n = 4, 4

b = np.array([400, 800, 200, 800])
c = np.array([
    [5, 3, 6, 2],
    [3, 4, 5, 6],
    [7, 5, 6, 4],
    [4, 8, 5, 3],
])
lb = np.array([300, 700, 200, 600])
ub = np.array([500, 1000, 400, 1000])
r = np.array([8, 10, 19, 6]) * 3
s = np.array([5, 6, 6, 3]) * 3

a_list = np.array([
    [900, 700, 600, 0],
    [500, 1100, 600, 0],
    [500, 700, 1000, 0],
    [500, 700, 600, 400],
])
p_list = np.array([
    [12, 3, 6, 0],
    [9, 5, 6, 0],
    [9, 3, 11, 0],
    [9, 3, 6, 10],
])
all_results = []
eye = np.eye(n)
for a, p in zip(a_list, p_list):
    linear_solver = LinearTransportProblem(m, n, a, b, p, c)
    linear_solver.solve()
    linear_solver.print()
    nonlinear_solver = NonlinearTransportProblem(m, n, a, p, c, lb, ub, r, s)
    nonlinear_solver.solve()
    nonlinear_solver.print()

    all_results.append([linear_solver, nonlinear_solver])
