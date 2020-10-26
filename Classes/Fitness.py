"""
Methods for fitness calculations.
"""

def get_fitness(spike_rate_A, spike_rate_B, plot_graph=False):
    """
    https://www.mathworks.com/help/matlab/ref/xcorr.html

    Takes two phenotypes as input at returns the best normalized cross-correlation score
    
    Can also plot the xcorr graph if flag is set
    """
    import numpy as np
    import matplotlib.pyplot as plt

    from Data import get_spikes_pheno

    # convert phenotype to 1D array of spike rates per timeunit. timeunit is set in get_spikes function    
    #spike_rate_A = get_spikes_pheno(phenotype_A)
    #spike_rate_B = get_spikes_pheno(phenotype_B) * 3

    # calls xcorr function in matplotlib. it returns a array
    corr = plt.xcorr(spike_rate_A, spike_rate_B, usevlines=True, normed=True, lw=2)
    fitness_score = np.amax(corr[1])

    # # lag of best fit (debugging)
    # lag = corr[0][np.where(corr[1]==fitness_score)]
    # print(lag)

    # plot graph (debugging)
    if plot_graph:
        plt.show()

    return (fitness_score)
