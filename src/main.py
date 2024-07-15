import numpy as np
from src.symbolic_regressor import SymbolicRegressor, visualize_ast
X = np.array(range(1,20))
X = X.reshape(1,-1)
y = np.square(X)

if __name__ == "__main__":
    sr = SymbolicRegressor()
    res = sr.fit(X,y)
    sorted_trees = sr.get_trees_sorted_by_cost(res)

    def get_cost(tree):
        return np.mean(tree.evaluate(X)-y)
    
    # print("_"*30 + "TREE ONE" + "_"*30)
    # print_tree(sorted_trees[0])
    # print(get_cost(sorted_trees[0]))

    # print("_"*30 + "TREE TWO" + "_"*30)
    # print_tree(sorted_trees[25])
    # print(get_cost(sorted_trees[25]))
    visualize_ast(sorted_trees[0])
    print(sorted_trees[0].evaluate(X) - y)
    breakpoint()
