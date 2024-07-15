import numpy as np

class Power:

    def __init__(self):
        self.a = None
        self.b = None
        self.num_args = 2

    def forward(self, a, b):
        self.a = a
        self.b = b
        
        # Compute log(abs(a)) * b element-wise
        with np.errstate(divide='ignore', invalid='ignore'):
            log_result = np.abs(a).astype(np.float64)
            np.log(log_result, out=log_result)
            log_result *= b

        # Create a mask for where overflow would occur
        overflow_mask = log_result > np.log(np.finfo(np.float64).max)
        
        # Compute the result using np.power
        with np.errstate(over='ignore', under='ignore'):
            result = np.power(a, b)
        
        # Where overflow occurred, replace with max float64 value (preserving sign)
        max_val = np.finfo(np.float64).max
        result = np.where(overflow_mask, np.sign(a) * max_val, result)
        
        # Handle special cases
        result = np.where(np.isnan(result), np.sign(a) * max_val, result)
        result = np.where(np.isinf(result), np.sign(result) * max_val, result)
        
        return np.clip(result,1,100)

    def backward(self):
        return [self.get_derivative_wrt_base(), self.get_derivative_wrt_exponent()]
    
    def get_derivative_wrt_base(self):
        return self.b*self.a**(self.b-1)
    
    def get_derivative_wrt_exponent(self):
        return np.log(self.b) * self.b**self.a

