from typing import Union
from collections import deque
import numpy as np
from src.utils import get_random_index, get_random_float
import copy
import random
import math


class ASTNode:

    def __init__(self, children=[], operation=None, level=0):
        self.children = children
        self.operation = operation
        self.level = level

    def __str__(self):
        return str(self.operation)

    def evaluate(self, X) -> float:
        result = self.operation.forward(*[child.evaluate(X) for child in self.children])
        return result

    def swap_nodes(self, other):
        # clone trees as not to screw them up in case we keep 
        # them with elitism or something
        self_copy = copy.deepcopy(self)
        other_copy = copy.deepcopy(other)

        self_nodes = self_copy.get_parent_nodes() 
        other_nodes = other_copy.get_parent_nodes()

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
        
    def get_parent_nodes(self) -> list:
        nodes = []
        stack = [self]
        while len(stack) > 0:
            node = stack.pop()
            if node.children:
                nodes.append(node)
                for child in node.children:
                    stack.append(child)
        return nodes
    
    def tree_size(self):
        if not self.children:
            return 1
        count = 1
        for child in self.children:
            count += child.tree_size()
        return count
    

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

from anytree import Node, RenderTree

def astnode_to_anytree(ast_node, parent=None):
    """
    Convert an ASTNode to an anytree Node for visualization.
    
    :param ast_node: The ASTNode to convert
    :param parent: The parent anytree Node (used in recursion)
    :return: An anytree Node representing the ASTNode
    """
    # Create a name for the node based on its type and attributes
    if isinstance(ast_node, ASTNode):
        if ast_node.operation:
            name = f"{ast_node.operation.__class__.__name__} id={id(ast_node)}"
        else:
            if isinstance(ast_node, Constant):
                name = f"{ast_node.__class__.__name__} id={id(ast_node)}(value={ast_node.value[0][0]})"
            elif isinstance(ast_node, Variable):
                name = f"{ast_node.__class__.__name__} id={id(ast_node)}(index={ast_node.index_of_value})"
            else:
                name = ast_node.__class__.__name__

    # Create the anytree Node
    tree_node = Node(name, parent=parent)

    # Recursively convert children
    if hasattr(ast_node, 'children'):
        for child in ast_node.children:
            astnode_to_anytree(child, parent=tree_node)

    return tree_node

# Function to visualize the tree
def visualize_ast(root_node):
    """
    Visualize an AST using anytree.
    
    :param root_node: The root ASTNode of your tree
    """
    # Convert ASTNode tree to anytree structure
    anytree_root = astnode_to_anytree(root_node)

    # Print ASCII representation
    print("ASCII Tree Representation:")
    for pre, _, node in RenderTree(anytree_root):
        print(f"{pre}{node.name}")

# Example usage:
if __name__ == "__main__":
    root = ASTNode(operation=None)
    const_node = Constant(value=3.14)
    var_node = Variable(index_of_value=1)
    root.children = [const_node, var_node]
    visualize_ast(root)


    