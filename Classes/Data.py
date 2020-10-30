"""
Methods for data processing.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_spikes_file(filename, recording_start=0, recording_len=30*60):
    # cleaning data, making array
    f = open("../Resources/" + filename, "r")
    data_points = [line.split(" ") for line in f]
    data_points = np.array(
        [(row[0].rstrip(), row[1].rstrip()) for row in data_points], 
        dtype=[("t", "float64"), ("electrode", "int64")])

    # edit to requested recording length
    start_index, stop_index = np.searchsorted(data_points["t"], [recording_start, recording_start+recording_len])
    data_points = data_points[start_index:stop_index]

    # time_coef = 1000 # bin width [ms]

    return get_spikes_pheno(data_points, recording_len)


def get_spikes_pheno(phenotype, recording_len):
    # time_coef = 1000 # bin width [ms]
    # spikes = []
    # start_time = int(phenotype[0]["t"])
    # for timestamp in phenotype["t"]:
    #     spikes.append(int(
    #         float(timestamp) * (1000/time_coef)
    #         ))
    
    # firing_rate = []
    # for n in spikes:
    #     if n >= len(firing_rate) + start_time:
    #         firing_rate.append(1)
    #     else:
    #         firing_rate[n-start_time] += 1
    # return np.array(firing_rate, dtype=np.float)

    array_wide_spikes_per_second = pd.cut(
        phenotype["t"], 
        bins=pd.interval_range(start=0, end=recording_len), 
        precision=0
    )
    return np.array(array_wide_spikes_per_second.value_counts().tolist(), dtype="float64")

    
def read_recording(filename, recording_start=0, recording_len=30*60):
    """
    Takes as input recording of experimental data as text file 
    Returns a phenotype
    
    """

    # cleaning data, making array
    f = open("../Resources/" + filename, "r")
    data_points = [line.split(" ") for line in f]
    data_points = np.array(
        [(row[0].rstrip(), row[1].rstrip()) for row in data_points], 
        dtype=[("t", "float64"), ("electrode", "int64")])

    # edit to requested recording length
    start_index, stop_index = np.searchsorted(data_points["t"], [recording_start, recording_start+recording_len])
    data_points = data_points[start_index:stop_index]

    f.close
    return data_points
    