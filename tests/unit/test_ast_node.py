from src.ast_node import ASTNode, Constant, Variable
from src.operations.multiply import Multiply
from src.operations.add import Add
from src.operations.power import Power

def test_evaluate():
    parent = ASTNode(operation=Add())
    child_one = Constant(4)
    child_two = Constant(6)
    parent.children = [child_one, child_two]
    assert parent.evaluate([]) == 10

def test_initialize_ast_node_randomly():
    node = ASTNode.initialize_randomly(**{"operations": [Multiply]})
    assert type(node.operation) is Multiply

def test_initialize_variable_randomly():
    node = Variable.initialize_randomly(**{"X": [1]})
    assert node.evaluate(np.array([1,2,3])) == 2