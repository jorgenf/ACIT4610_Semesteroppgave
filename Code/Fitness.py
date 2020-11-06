"""
Methods for fitness calculations.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from Data import get_spikes_pheno


def get_fitness_corr(spike_rate_X, spike_rate_control, plot_graph=False):
    """
    https://www.mathworks.com/help/matlab/ref/xcorr.html
    Takes two phenotypes as input at returns the best normalized cross-correlation score
    Can also plot the xcorr graph if flag is set
    Calls xcorr function in matplotlib which returns an array
    """
    #   Check if array is only zeros
    if spike_rate_X.any():
        corr = plt.xcorr(spike_rate_X, spike_rate_control, usevlines=True, normed=True, lw=2, maxlags=1)
        fitness_score = np.amax(corr[1])
    else:
        fitness_score = 0.0

    #   Debugging purposes
    if plot_graph:
        # # lag of best fit
        lag = corr[0][np.where(corr[1] == fitness_score)]
        print(lag)
        plt.show()

    return "NA", "NA", fitness_score


def get_fitness_spike_dist(spike_rate_x, spike_rate_control, order=6, threshold=0.6):
    """
    Calculates fitness from a combination of burst correlation
    and average distance between the spikes per second data points.
    Counts the number of bursts by checking if the number of spikes exceed a threshold relative to the maximum value.
    """
    #   Calculate the maximum value in the reference data
    max_val = max([spike_rate_control[i] for i in signal.argrelextrema(spike_rate_control, np.greater, order=order)[0]])
    #   Look for bursts in the experiment data
    control_bursts = signal.argrelextrema(spike_rate_control, np.greater, order=order)[0]
    #   Look for bursts in the model data
    x_bursts = signal.argrelextrema(spike_rate_x, np.greater, order=order)[0]
    #   Count the number of bursts, values that exceed the threshold.
    adj_control_bursts = len(
        [spike_rate_control[i] for i in control_bursts if spike_rate_control[i] >= max_val * threshold])
    adj_x_bursts = len(
        [spike_rate_x[i] for i in x_bursts if spike_rate_x[i] >= max_val * threshold])
    #   Calculate correlation between bursts in the reference data and the model data
    burst_corr = (adj_control_bursts - abs(adj_control_bursts - adj_x_bursts)) / adj_control_bursts
    if burst_corr < 0:
        burst_corr = 0
    #   Sort spike rate lists
    a = sorted(spike_rate_control)
    b = sorted(spike_rate_x)
    dist = []
    #   Append the distance between each data point in the lists to a new list.
    for i, j in zip(a, b):
        dist.append(abs(i - j))
    #   Calculate the average distance
    avg_dist = (max(spike_rate_control) - (sum(dist) / len(dist))) / max(spike_rate_control)
    if avg_dist < 0:
        avg_dist = 0
    fitness = (burst_corr + avg_dist) / 2
    return burst_corr, avg_dist, fitness


def get_fitness_dist(spike_rate_x, spike_rate_control):
    """
    Sorts the lists of spike data from both the experiment and the model.
    The average distance between them is returned as the fitness score.
    """
    #   Sort spike rate lists
    a = sorted(spike_rate_control)
    b = sorted(spike_rate_x)
    dist = []
    #   Append the distance between each data point in the lists to a new list.
    for i, j in zip(a, b):
        dist.append(abs(i - j))
    #   Calculate the average distance
    avg_dist = (np.mean(spike_rate_control) - (np.mean(dist))) / np.mean(spike_rate_control)
    if avg_dist < 0:
        avg_dist = 0
    fitness = avg_dist
    return "NA", avg_dist, fitness
