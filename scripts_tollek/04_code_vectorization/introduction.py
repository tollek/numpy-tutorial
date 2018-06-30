#!/usr/bin/python3.6
import sys
sys.path.append('../../')
sys.path.append('/home/tollek/workspace/gocode/src/github.com/rougier/numpy-tutorial')

import numpy as np
from tools.tools import *
import random

def add_python(Z1, Z2):
    return [z1 + z2 for (z1,z2) in zip(Z1, Z2)]

x = [1, 2, 3, 4]
y = [10, 20, 30, 40]
print(add_python(x, y))

# introduction of numpy implementation
def add_numpy(Z1, Z2):
    return np.add(Z1, Z2)

print(add_numpy(x, y))
info(add_numpy(x, y))

# performance of python and numpy implementations
Z1 = random.sample(range(1000), 100)
Z2 = random.sample(range(1000), 100)
timeit("add_python(Z1, Z2)", globals())
timeit("add_numpy(Z1, Z2)", globals())

# issues, when Z1 and Z2 aren't flat lists
Z1 = [[1, 2], [3, 4]]
Z2 = [[5, 6], [7, 8]]
print(Z1 + Z2)
print(add_python(Z1, Z2))
print(add_numpy(Z1, Z2))
