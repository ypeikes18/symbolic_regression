from src.operations.add import Add
import numpy as np

def test_init():
    add = Add()
    assert add.num_args == 2
    assert add.a is None and add.b is None

def test_forward():
    a = np.array([1,2,3])
    b = np.array([4,5,6])
    assert np.array_equal(Add().forward(a,b), np.array([5,7,9]))