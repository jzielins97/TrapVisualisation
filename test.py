import numpy as np
import os

script_dir = os.path.dirname(__file__)
print(script_dir)
potential_matrix_path = os.path.join(script_dir,"potential-simulation", "ElectrodesPotentialMap.txt")
with open(potential_matrix_path, 'r') as f:
    __POTENTIAL_MATRIX = np.array([[float(value) for value in l.strip().split("\t")[1:2049]] if l.strip().split("\t")[0] != 'C1' else [0]*2048 for l in f.readlines()])

print(__POTENTIAL_MATRIX)

