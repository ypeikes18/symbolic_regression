import random
import numpy as np

def get_random_index(list_):
    if type(list) is np.ndarray:
        return random.randint(0, list_.shape[0]-1)
    return random.randint(0, len(list_)-1)

def get_random_float(start, stop, step=1):
    num_steps = int((stop - start))/step
    random_index = random.randint(0, num_steps)
    return start + random_index * step

