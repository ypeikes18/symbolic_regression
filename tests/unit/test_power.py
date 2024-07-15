from src.operations.power import Power
import numpy as np

def test_init():
    power = Power()
    assert power.num_args == 2
    assert power.a is None and power.b is None

def test_forward():
    a = np.array([1,2,3])
    b = np.array([2,2,2])
    # WHEN results aren't clipped
    assert np.array_equal(Power().forward(a,b), np.array([1,4,9]))

    b = np.array([200,200,200])
    # WHEN results aren't clipped
    breakpoint()
    assert np.array_equal(Power().forward(a,b), np.array([1.0,100.0,100.0]))