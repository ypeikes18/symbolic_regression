import numpy as np
import scipy.constants as const

def get_multivariate_synthetic_data(num_samples):
    var_1 = np.random.randn(0, 10**9, num_samples)
    var_2 = np.random.uniform(0, 10**9, num_samples)

    X = np.vstack((var_1, var_2))
    return X

def get_gravity_variables(*,num_samples):
    mass_one = np.random.uniform(1, 10**10, num_samples)
    mass_two = np.random.uniform(1, 10, num_samples)
    distance = np.random.uniform(1, 10**2, num_samples)
    return np.vstack((mass_one, mass_two, distance))

def compute_gravitational_force(X):
    G = const.G
    mass_one = X[0, :]  
    mass_two = X[1, :]  
    distance = X[2, :]  
    return G * mass_one * mass_two / distance**2