from src.operations.multiply import Multiply
from src.operations.add import Add
from src.operations.power import Power
from src.operations.divide import Divide


from src.ast_node import ASTNode, Constant, Variable
import numpy as np
import random
import heapq

default_params = {
    "operations": [Multiply, Add, Power, Divide],
    "num_nodes": 100,
    "start": 1,
    "stop": 6,
    "step":1,
    "max_tree_size": 100,
    "num_generations": 15,
    "num_offspring": 400,
    "initial_population_size": 500,
    "crossover_rate": 0.8, # TODO some of these really need to be functions so they can be more dynamic
    "mutation_rate": 0.25,
    "mutation_types": ['point', 'subtree', 'shrink', 'expand'],
    "tournament_size": 4,
    "elitism":100,
    "num_mediocre_survivors":0,
    "node_count_penalty_coefficient": 0.1,
    "num_processes": 1
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
        self.elitism = params.get("elitism") or default_params.get("elitism")
        self.num_offspring = params.get("num_offspring") or default_params.get("num_offspring")
        self.tournament_size = params.get("tournament_size") or default_params.get("tournament_size")
        self.num_mediocre_survivors = params.get("num_mediocre_survivors") or default_params.get("num_mediocre_survivors")
        self.node_count_penalty_coefficient = params.get("node_count_penalty_coefficient") or default_params.get("node_count_penalty_coefficient")
        self.num_processes = params.get("num_processes") or default_params.get("num_processes")
        self.X = None
        self.costs = []


    def fit(self, X, y):
        self.X = X
        self.y = y
        population = self.get_initial_population(X)
        remaining_generations = self.num_generations - 1
        while remaining_generations > 0:
            print(f"Generations remaining: {remaining_generations}")
            population = self.get_next_generation(population)
            best_tree = self.get_trees_sorted_by_cost(population)[0]
            lowest_cost = self.get_cost(best_tree)
            self.costs.append(lowest_cost)
            print(f"lowest cost: {lowest_cost}")
            remaining_generations -=1
        return population


    def get_initial_population(self, X):
        params = {**default_params, "X": X} # TODO fix this so it takes in the models actual params
        return [ASTNode.build_tree(**params) for _ in range(self.initial_population_size)]

    def get_next_generation(self, population):
        return self.get_survivors(population) + self.get_all_offspring(population)

    def get_trees_sorted_by_cost(self, trees):
        # TODO maybe modify to only use top n and with a heap or generate by cost in the first place
        return sorted(trees, key=self.get_cost)

    def get_survivors(self, population):
        sorted_population = self.get_trees_sorted_by_cost(population)
        return self.get_elites(sorted_population) + self.get_mediocre_survivors(sorted_population)

    def get_elites(self, sorted_population):
        return sorted_population[:self.elitism]

    def get_mediocre_survivors(self, sorted_population):
        return random.sample(sorted_population[self.elitism:], self.num_mediocre_survivors)

    def get_all_offspring(self, population):
        offspring = []
        for _ in range(self.num_offspring):
            parent_one = self.select_parent(population)
            parent_two = self.select_parent(population)
            child = parent_one.swap_nodes(parent_two)
            self.mutate(child)
            offspring.append(child)
        return offspring

    def select_parent(self, population):
        competitors = random.sample(population, self.tournament_size)
        return min(competitors, key=self.get_cost)

    def mutate(self, node):
        self.point_wise_mutate(node)

    def point_wise_mutate(self, tree):
        for node in tree:
            if random.random() <= self.mutation_rate:
                node.change_value(**{**default_params, "X": self.X}) # TODO fix this so it takes in the models actual params

    def get_cost(self, tree):
        def num_levels(root):
            if not root.children:
                return 1
            return 1 + max([num_levels(child) for child in root.children])
        costs = np.power(tree.evaluate(self.X)-self.y,2) + num_levels(tree)*self.node_count_penalty_coefficient
        return np.mean(costs)


