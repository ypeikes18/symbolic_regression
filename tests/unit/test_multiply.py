from src.operations.multiply import Multiply
import numpy as np

def test_init():
    multiply = Multiply()
    assert multiply.num_args == 2
    assert multiply.a is None and multiply.b is None

def test_forward():
    a = np.array([1,2,3])
    b = np.array([2,2,2])
    assert np.array_equal(Multiply().forward(a,b), np.array([2,4,6]))