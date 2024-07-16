import numpy as np
from src.symbolic_regressor import SymbolicRegressor, visualize_ast

def get_multivariate_synthetic_data(num_samples):
    var_1 = np.random.uniform(0.01, 10, num_samples)
    var_2 = np.random.uniform(0.1, 10, num_samples)

    X = np.vstack((var_1, var_2))
    return X

X = get_multivariate_synthetic_data(10)
y = np.array([col[0]**3 + col[1] for col in X.T])

if __name__ == "__main__":
    sr = SymbolicRegressor()
    res = sr.fit(X,y)
    sorted_trees = sr.get_trees_sorted_by_cost(res)

    visualize_ast(sorted_trees[0])
    print(sorted_trees[0].evaluate(X) - y)
    breakpoint()
