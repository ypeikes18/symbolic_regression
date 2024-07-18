import numpy as np

class Cosine:

    def __init__(self):
        self.a = None
        self.b = None
        self.num_args = 1

    def forward(self, a):
        self.a = a
        return np.cos(a)
    
    def backward(self):
        return [self.b, self.a]