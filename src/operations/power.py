import numpy as np

class Power:

    def __init__(self):
        self.a = None
        self.b = None
        self.num_args = 2

    def forward(self, a, b):
        a = np.array(a)
        b = np.array(b)
        try:
            result = np.power(a, b)
        except:
            result =  1 / np.power(a, np.abs(b))
        return np.clip(result,1,100) # TODO unharcode

    def backward(self):
        return [self.get_derivative_wrt_base(), self.get_derivative_wrt_exponent()]
    
    def get_derivative_wrt_base(self):
        return self.b*self.a**(self.b-1)
    
    def get_derivative_wrt_exponent(self):
        return np.log(self.b) * self.b**self.a

