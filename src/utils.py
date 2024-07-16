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

def get_subscript(n):
    """
    Convert a number to its subscript string representation.
    
    Parameters:
    n (int): The number to convert to subscript.
    
    Returns:
    str: The subscript string representation of the number.
    """
    subscript_chars = {
        '0': '\u2080', '1': '\u2081', '2': '\u2082', '3': '\u2083', '4': '\u2084',
        '5': '\u2085', '6': '\u2086', '7': '\u2087', '8': '\u2088', '9': '\u2089'
    }
    return ''.join(subscript_chars[digit] for digit in str(n))

def get_subscript_string(n: int) -> str:
    return 'X' + get_subscript(n)

