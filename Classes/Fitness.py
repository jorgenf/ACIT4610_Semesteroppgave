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



def get_fitness_2(spike_rate_x, spike_rate_control, order = 6):

    max_val = max([spike_rate_control[i] for i in signal.argrelextrema(spike_rate_control, np.greater, order=order)[0]])
    control_bursts = signal.argrelextrema(spike_rate_control, np.greater, order=order)[0]
    x_bursts = signal.argrelextrema(spike_rate_x, np.greater, order=order)[0]
    adj_control_bursts = len([spike_rate_control[i] for i in control_bursts if spike_rate_control[i] >= max_val / 2])
    adj_x_bursts = len([spike_rate_x[i] for i in x_bursts if spike_rate_x[i] >= max_val / 2])

    burst_corr = (adj_control_bursts - abs(adj_control_bursts - adj_x_bursts)) / adj_control_bursts
    if burst_corr < 0:
        burst_corr = 0

    a = sorted(spike_rate_control)
    b = sorted(spike_rate_x)
    dist = []
    #print("MAX",max(spike_rate_control))
    for i, j in zip(a, b):
        dist.append(abs(i - j))
    avg_dist = (max(spike_rate_control)/2 - sum(dist) / len(dist)) / max(spike_rate_control)/2
    if avg_dist < 0:
        avg_dist = 0
    fitness = (burst_corr + avg_dist) / 2
    return burst_corr, avg_dist, fitness


