"""
Only for testing get_fitness
Not part of module
"""

from Fitness import get_fitness

def read_recording(filename, recording_start=0, recording_len=30*60):
    from operator import itemgetter
    import numpy as np
    import pandas as pd

    # cleaning data, making array
    f = open(filename, "r")
    data_points = [line.split(" ") for line in f]
    data_points = np.array(
        [(row[0].rstrip(), row[1].rstrip()) for row in data_points], 
        dtype=[("t", "float64"), ("electrode", "int64")])

    # edit to requested recording length
    start_index, stop_index = np.searchsorted(data_points["t"], [recording_start, recording_start+recording_len])
    data_points = data_points[start_index:stop_index]

    f.close
    return data_points

filepath = r"..\Resources\Dense - 2-1-20.spk.txt"
x_ptype = read_recording(filepath, recording_start=59, recording_len=20)
y_ptype = read_recording(filepath, recording_start=60, recording_len=20)

print("Fitness:", get_fitness(x_ptype, y_ptype, plot_graph=True))