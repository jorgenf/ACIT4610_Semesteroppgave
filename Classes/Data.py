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


def raster_plot(phenotype_A, phenotype_B, bin_size):
    """
    Takes two phenotypes as input and plot them side-by-side as raster plot and histogram

    Assumes "phenotype_X" is a list of lists or 2D numpy array similar to:
    [[.00396, 56],
    [0.05284, 16],
    [0.05800, 15],
    ...,
    [A, B]]
    Where A is a timestamp and B is electrode ID (must be a integer between 0-63)

    To create histogram it is necessary to specify bin-size. For spikes per second "bin_size" = simulation length [seconds] 

    """

    # check if input is correct format    
    phenotype_A = np.array(
        [(row[0], row[1]) for row in phenotype_A], 
        dtype=[("t", "float64"), ("electrode", "int64")])
    phenotype_B = np.array(
        [(row[0], row[1]) for row in phenotype_B], 
        dtype=[("t", "float64"), ("electrode", "int64")])

    # sort spikes by electrode
    A_spikes_per_array = [ [] for _ in range(64)]
    for row in phenotype_A:
        A_spikes_per_array[row[1]].append(row[0])

    B_spikes_per_array = [ [] for _ in range(64)]
    for row in phenotype_B:
        B_spikes_per_array[row[1]].append(row[0])

    # initiate plot
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)

    # make raster plots
    ax1.eventplot(
        A_spikes_per_array,
        linewidths=0.5
        )
    ax1.set_xlabel("Seconds")
    ax1.set_ylabel("Electrode ID")
    ax1.set_title("Neural raster plot")
    
    ax2.eventplot(
        B_spikes_per_array,
        linewidths=0.5,
        color = "black"
        )
    ax2.set_xlabel("Seconds")
    ax2.set_title("Simulation raster plot")

    # make histograms
    ax3.hist(phenotype_A["t"], bins=bin_size)
    ax3.set_xlabel("Seconds")
    ax3.set_ylabel("Spikes per second")

    ax4.hist(phenotype_B["t"], bins=bin_size, color="black")
    ax4.set_xlabel("Seconds")

    plt.show()


def read_recording(filename, recording_start=0, recording_len=30*60):
    """
    Takes as input recording of experimental data as text file 
    Returns a phenotype
    
    """

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