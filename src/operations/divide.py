import numpy as np

class Divide:

    def __init__(self):
        self.a = None
        self.b = None
        self.num_args = 2

    def forward(self, a, b):
        self.a = a
        self.b = b
        return np.divide(a,b)
    
    def backward(self):
        pass # TODO