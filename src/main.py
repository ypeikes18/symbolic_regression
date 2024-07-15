from src.operations.multiply import Multiply
from src.operations.add import Add
from src.operations.power import Power


from src.ast_node import ASTNode, Constant, Variable, print_tree, visualize_ast
import numpy as np
import random
import heapq

X = np.array(range(1,20))
X = X.reshape(1,-1)

y = np.square(X) + 2

initial_population_size = 500
crossover_rate = 0.8
mutation_rate = 0.2
tournament_size = 7
generations = 50
elitism = 12

#start, stop, step, X, num_nodes, max_depth
default_params = {
    "operations": [Multiply, Add],
    "num_nodes": 100,
    "start": 1,
    "stop": 3,
    "step": 1,
    "max_tree_size": 100,
    "num_generations": 50
}

def get_trees_by_cost(trees):
    # TODO modify to only use top n and with a heap or generate by cost
    return sorted(trees, key=lambda tree: tree.evaluate(X))

initial_population = [ASTNode.build_tree(**{**default_params, "X": X}) for i in range(initial_population_size)]

population = initial_population
current_generation_number = 1
while current_generation_number < default_params["num_generations"]:
    sorted_population = get_trees_by_cost(population)
    elites = sorted_population[:elitism]
    current_generation_number += 1

breakpoint()
