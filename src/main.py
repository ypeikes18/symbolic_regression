import numpy as np
from src.symbolic_regressor import SymbolicRegressor
import multiprocessing as mp
from src.utils.md_utils import create_md_tree

num_samples = 100
x0_range = (1, 100)
x1_range = (1, 100)
x2_range = (1, 100)  # Avoid zero to prevent division by zero # TODO fix that

# Generate random values for x0, x1, and x2
x0 = np.arange(num_samples)
x1 = np.random.uniform(x1_range[0], x1_range[1], num_samples)
x2 = np.random.uniform(x2_range[0], x2_range[1], num_samples)[::-1]
X = np.vstack((x0,x1))
# Compute the target values using the expression
y = (x0 * x1)/5

if __name__ == "__main__":
    sr = SymbolicRegressor(num_processes=4)
    res = sr.fit(X,y)
    create_md_tree(res[0])
