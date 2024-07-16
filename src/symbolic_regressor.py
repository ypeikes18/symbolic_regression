from src.operations.multiply import Multiply
from src.operations.add import Add
from src.operations.power import Power


from src.ast_node import ASTNode, Constant, Variable, visualize_ast
import numpy as np
import random
import heapq

default_params = {
    "operations": [Multiply, Add, Power],
    "num_nodes": 100,
    "start": -3,
    "stop": 3,
    "step": 0.1,
    "max_tree_size": 100,
    "num_generations": 50,
    "num_offspring": 300,
    "initial_population_size": 500,
    "crossover_rate": 0.8, # TODO some of these really need to be functions so they can be more dynamic
    "mutation_rate": 0.2,
    "mutation_types": ['point', 'subtree', 'shrink', 'expand'],
    "tournament_size": 7,
    "generations": 50,
    "elitism":200
}
class SymbolicRegressor:

    def __init__(self, **params):
        self.operations = params.get("operations") or default_params.get("operations")
        self.num_nodes = params.get("num_nodes") or default_params.get("num_nodes")
        self.start = params.get("start") or default_params.get("start")
        self.stop = params.get("stop") or default_params.get("stop")
        self.step = params.get("step") or default_params.get("step")
        self.max_tree_size = params.get("max_tree_size") or default_params.get("max_tree_size")
        self.num_generations = params.get("num_generations") or default_params.get("num_generations")
        self.num_offspring = params.get("num_offspring") or default_params.get("num_offspring")
        self.initial_population_size = params.get("initial_population_size") or default_params.get("initial_population_size")
        self.crossover_rate = params.get("crossover_rate") or default_params.get("crossover_rate")
        self.mutation_rate = params.get("mutation_rate") or default_params.get("mutation_rate")
        self.tournament_size = params.get("tournament_size") or default_params.get("tournament_size")
        self.generations = params.get("generations") or default_params.get("generations")
        self.elitism = params.get("elitism") or default_params.get("elitism")
        self.num_offspring = params.get("num_offspring") or default_params.get("num_offspring")
        self.tournament_size = params.get("tournament_size") or default_params.get("tournament_size")
        self.X = None

    def fit(self, X, y):
        self.X = X
        self.y = y
        population = self.get_initial_population(X)
        remaining_generations = self.generations - 1
        while remaining_generations > 0:
            print(f"Generations remaining: {remaining_generations}")
            population = self.perform_evolution(population)
            remaining_generations -=1
        return population
    
    def get_initial_population(self, X):
        params = {**default_params, "X": X} # TODO fix this so it takes in the models actual params
        return [ASTNode.build_tree(**params) for _ in range(self.initial_population_size)]

    def perform_evolution(self, population):
        return self.get_elites(population) + self.get_all_offspring(population)

    def get_trees_sorted_by_cost(self, trees):
        # TODO maybe modify to only use top n and with a heap or generate by cost in the first place
        return sorted(trees, key=self.get_cost)

    def get_elites(self, population):
        return self.get_trees_sorted_by_cost(population)[:self.elitism]    
    
    def get_all_offspring(self, population):
        offspring = []
        for _ in range(self.num_offspring):
            parent_one = self.select_parent(population)
            parent_two = self.select_parent(population)
            child = parent_one.swap_nodes(parent_two)
            offspring.append(child)
        return offspring

    def select_parent(self, population):
        competitors = random.sample(population, self.tournament_size)
        return min(competitors, key=self.get_cost)

    def get_cost(self, tree): # TODO this needs to get X and y normally 
        return np.mean(abs(tree.evaluate(self.X)-self.y))
