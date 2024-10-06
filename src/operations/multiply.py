import numpy as np

class Multiply:

    def __init__(self):
        self.a = None
        self.b = None
        self.num_args = 2

    def forward(self, a, b):
        self.a = a
        self.b = b
        return np.multiply(a,b)

    def backward(self):
        return [self.b, self.a]

    def __str__(self):
        return self.__class__.__name__
