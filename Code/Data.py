"""
Methods for data processing.
"""
import numpy as np
import pandas as pd


def get_spikes_file(filename, recording_start=0, recording_len=30*60):
    """
    Get spikes per electrode data from a file.
    Uses helper method get_spikes_pheno.
    Return: Numpy Array
    """
    #   Clean up the data and create a numpy array from it
    f = open("../Resources/" + filename, "r")
    data_points = [line.split(" ") for line in f]
    data_points = np.array(
        [(row[0].rstrip(), row[1].rstrip()) for row in data_points], 
        dtype=[("t", "float64"), ("electrode", "int64")])
    
    #   Edit according to specified recording length
    start_index, stop_index = np.searchsorted(data_points["t"], [recording_start, recording_start+recording_len])
    data_points = data_points[start_index:stop_index]

    return get_spikes_pheno(data_points, recording_len)


def get_spikes_pheno(phenotype, recording_len):
    """
    Get spikes per electrode data from input phenotype.
    Return: Numpy Array
    """
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
    #   Clean up the data and create a numpy array from it
    f = open("../Resources/" + filename, "r")
    data_points = [line.split(" ") for line in f]
    data_points = np.array(
        [(row[0].rstrip(), row[1].rstrip()) for row in data_points], 
        dtype=[("t", "float64"), ("electrode", "int64")])

    #   Edit according to specified recording length
    start_index, stop_index = np.searchsorted(data_points["t"], [recording_start, recording_start+recording_len])
    data_points = data_points[start_index:stop_index]
    f.close
    return data_points
