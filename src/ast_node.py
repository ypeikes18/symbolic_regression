from typing import Union
from collections import deque
import numpy as np
from src.utils.utils import get_random_index, get_random_float
import copy
import random
import math


class ASTNode:

    def __init__(self, children=[], operation=None, level=0):
        self.children = children
        self.operation = operation
        self.level = level
        self.evaluated_value = None

    def __str__(self):
        return str(self.operation)


    def evaluate(self, X) -> float:
        if self.evaluated_value is not None:
            return self.evaluated_value
        result = self.operation.forward(*[child.evaluate(X) for child in self.children])
        self.evaluated_value = result
        return result

    def swap_nodes(self, other):
        # clone trees as not to screw them up in case we keep
        # them with elitism or something
        self_copy = copy.deepcopy(self)
        self_copy.evaluated_value = None
        other_copy = copy.deepcopy(other)
        other_copy.evaluated_value = None

        self_nodes = self_copy.get_nodes()
        other_nodes = other_copy.get_nodes()

        # select random node from each
        self_node = random.choice(self_nodes)
        other_node = random.choice(other_nodes)

        # pick random index from indices in node.children
        swap_index_1 = get_random_index(self_node.children)
        swap_index_2 = get_random_index(other_node.children)

        self_node.children[swap_index_1] = other_node.children[swap_index_2]
        return self_copy


    @classmethod
    def initialize_randomly(cls, **params):
        # operations in a node are instances
        operation_class = random.choice(params['operations'])
        return cls(operation=operation_class(), children=[])


    def get_num_children(self):
        return self.operation.num_args

       # swap in the child that was selected from swap_index_1 to swap_index_2

    @classmethod
    def build_tree(cls,**params):
        """
        max_tree_size = max number of nodes
        """
        options = [ASTNode, Constant, Variable]
        num_allowed_nodes = params["max_tree_size"] - 1
        root =  ASTNode.initialize_randomly(**params)
        queue = deque([root])
        while queue:
            current = queue.pop()
            if type(current) is ASTNode:
                for _ in range(current.get_num_children()):
                    child = random.choice(options).initialize_randomly(**params)
                    child.level = current.level + 1
                    queue.appendleft(child)
                    current.children.append(child)
                    num_allowed_nodes-=1
        return root

    def get_nodes(self,include_leaves=False) -> list:
        nodes = []
        stack = [self]
        while len(stack) > 0:
            node = stack.pop()
            if node.children or include_leaves:
                nodes.append(node)
                for child in node.children:
                    stack.append(child)
        return nodes

    # TODO this might be able to replace all the dfs traversals
    def dfs_with_function(self, func):
        if not self.children:
            return [func(self)]
        res = [func(self)]
        for child in self.children:
            res.extend(child.dfs_with_function(func))
        return res

    def tree_size(self):
        if not self.children:
            return 1
        count = 1
        for child in self.children:
            count += child.tree_size()
        return count

    def __iter__(self):
        self.stack = [self]
        return self

    def __next__(self):
        if not self.stack:
            raise StopIteration
        current_node = self.stack.pop()
        self.stack.extend(reversed(current_node.children))
        return current_node

    def change_value(self, **params):
        operation_class = random.choice(params['operations'])
        self.operation = operation_class()

class Constant(ASTNode):

    def __init__(self, value: float):
        super().__init__()
        self.value = value

    # def __eq__(self, other):
    #     return self.value == other.value

    def __str__(self):
        return str(list(self.value))

    def evaluate(self, X=None):
        return self.value

    @classmethod
    def initialize_randomly(cls, **params):
        value = get_random_float(params["start"], params["stop"], params["step"])
        vector =  np.full(params["X"].shape,fill_value=value)
        return cls(vector)

    def change_value(self, **params):
        value = get_random_float(params["start"], params["stop"], params["step"])
        vector =  np.full(params["X"].shape,fill_value=value)
        self.value = vector


class Variable(ASTNode):

    def __init__(self, index_of_value: float):
        super().__init__()
        self.index_of_value = index_of_value

    def __str__(self):
        return f"X{self.index_of_value}"

    def __eq__(self, other):
        return self.index_of_value == other.index_of_value

    def evaluate(self, X):
        return X[self.index_of_value]

    @classmethod
    def initialize_randomly(cls, **params):
        i = get_random_index(params["X"])
        return cls(i)

    def change_value(self, **params):
        i = get_random_index(params["X"])
        self.index_of_value = i
