import numpy as np
from src.symbolic_regressor import SymbolicRegressor, visualize_ast

num_samples = 100
x0_range = (1, 100)
x1_range = (1, 100)
x2_range = (1, 100)  # Avoid zero to prevent division by zero

# Generate random values for x0, x1, and x2
x0 = np.arange(num_samples)
x1 = np.random.uniform(x1_range[0], x1_range[1], num_samples)
x2 = np.random.uniform(x2_range[0], x2_range[1], num_samples)
X = np.vstack((x0,x1))
# Compute the target values using the expression
y = (x0 * x1)/5

if __name__ == "__main__":
    import multiprocessing as mp
    def run(i):
        sr = SymbolicRegressor()
        res = sr.fit(X,y)
        sorted_trees = sr.get_trees_sorted_by_cost(res)
        return sorted_trees[0], sr.costs

    with mp.Pool(processes=4) as pool:
        results = pool.map(run, range(4))


    for tree, costs in results:
        visualize_ast(tree)
        print(costs)
    breakpoint()