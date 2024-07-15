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
default_params = {
    "operations": [Multiply, Add],
    "num_nodes": 100,
    "start": 1,
    "stop": 3,
    "step": 1,
    "max_tree_size": 100,
    "num_generations": 50,
    "initial_population_size": 500,
    "crossover_rate": 0.8, # TODO some of these really need to be functions so they can be more dynamic
    "mutation_rate": 0.2,
    "tournament_size": 7,
    "generations": 50,
    "elitism":12
}
class SymbolicRegressor:

    def __init__(self, **params):
        self.initial_population_size = params.get("initial_population_size") or default_params.get("initial_population_size")
        self.crossover_rate = params.get("crossover_rate") or default_params.get("crossover_rate")
        self.mutation_rate = params.get("mutation_rate") or default_params.get("mutation_rate")
        self.tournament_size = params.get("tournament_size") or default_params.get("tournament_size")
        self.generations = params.get("generations") or default_params.get("generations")
        self.elitism = params.get("elitism") or default_params.get("elitism")

    def fit(self, X):
        population = self.get_initial_population(X)
        remaining_generations = self.generations - 1
        while remaining_generations > 0:
            population = self.perform_evolution(population)
        return population
    
    def get_initial_population(self, X):
        params = {**default_params, "X": X}
        return [ASTNode.build_tree(**params) for _ in range(self.initial_population_size)]

    def perform_evolution(self):
        pass

    def get_trees_sorted_by_cost(self, trees):
        # TODO maybe modify to only use top n and with a heap or generate by cost in the first place
        def get_cost(tree): # TODO this needs to be a separate function
            return np.mean(abs(tree.evaluate(X)-y))
        return sorted(trees, key=get_cost)

    def get_elites(self, population):
        return population[:self.elitism]    
    








sr = SymbolicRegressor()
population = sr.get_initial_population(X)
sortd = sr.get_trees_sorted_by_cost(population)
breakpoint()
