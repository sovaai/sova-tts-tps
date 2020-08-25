import numpy as np


def prob2bool(prob):
    return np.random.choice([True, False], p=[prob, 1 - prob])