import numpy as np
from src.symbolic_regressor import SymbolicRegressor
from src.utils.md_utils import create_md_tree


x0 = np.array([1,2,3,4,5]) # 1,4,9 ,16,25
x1 = np.array([2,4,5,3,1]) # 4,8,10,6 ,2
                           # 5,12,19,22,27
                           # 49,0,49,100,225
X = np.vstack((x0,x1))

y = np.square(x0) + x1 * 2

if __name__ == "__main__":
    sr = SymbolicRegressor(num_processes=1)
    res = sr.fit(X,y)
    print(f"evaluating tree: {res[0].evaluate(X)}")
    create_md_tree(res[0])
    breakpoint()
