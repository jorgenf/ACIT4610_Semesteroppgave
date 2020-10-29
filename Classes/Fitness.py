"""
Methods for fitness calculations.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

from Data import get_spikes_pheno

def get_fitness(spike_rate_X, spike_rate_control, plot_graph=False):
    """
    https://www.mathworks.com/help/matlab/ref/xcorr.html

    Takes two phenotypes as input at returns the best normalized cross-correlation score
    
    Can also plot the xcorr graph if flag is set
    """

    # convert phenotype to 1D array of spike rates per timeunit. timeunit is set in get_spikes function    
    #spike_rate_X = get_spikes_pheno(phenotype_A)
    #spike_rate_control = get_spikes_pheno(phenotype_B)

    # calls xcorr function in matplotlib. it returns a array
    if spike_rate_X.any(): # check if array is only zeros
        corr = plt.xcorr(spike_rate_X, spike_rate_control, usevlines=True, normed=True, lw=2, maxlags=1) # maxlags should not be set, only for debugging
        fitness_score = np.amax(corr[1])
    else:
        fitness_score = 0.0

    # # lag of best fit (debugging)
    # lag = corr[0][np.where(corr[1]==fitness_score)]
    # print(lag)

    # plot graph (debugging)
    if plot_graph:
        plt.show()

    return fitness_score



def get_fitness_2(spike_rate_X, spike_rate_control):
    control_bursts = len(signal.argrelextrema(spike_rate_control, np.greater, order=3)[0])
    x_bursts = len(signal.argrelextrema(spike_rate_X, np.greater, order=3)[0])

    burst_corr = (control_bursts - abs(control_bursts - x_bursts)) / control_bursts

    a = sorted(spike_rate_control)
    b = sorted(spike_rate_X)
    dist = []
    for i, j in zip(a, b):
        dist.append(abs(i - j))
    avg_dist = (100 - sum(dist) / len(dist)) / 100
    fitness = (burst_corr + avg_dist) / 2
    return fitness


