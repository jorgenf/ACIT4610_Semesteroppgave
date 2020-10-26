"""
Methods for data processing.
"""


def get_spikes_file(file_name):
    """
    
    :param string_one: 
    :return: NumpyArray
    """""
    file = open("../Resources/"+file_name,"r")
    times = []
    nodes = []
    spikes = []
    for line in file:
        time, node = line.split(" ")
        times.append(time)
        nodes.append(node)
        spikes.append(int(float(time)*10))
    firing_rate = []
    for n in spikes:
        if n >= len(firing_rate):
            firing_rate.append(1)
        else:
            firing_rate[n] += 1
    return(firing_rate)


def get_spikes_pheno(phenotype):
    """

    :param string_one: 
    :return: NumpyArray
    """
    pass


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
    import matplotlib.pyplot as plt
    import numpy as np

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
    # print(phenotype_A["t"])
    ax3.hist(phenotype_A["t"], bins=bin_size)
    ax3.set_xlabel("Seconds")
    ax3.set_ylabel("Spikes per second")

    ax4.hist(phenotype_B["t"], bins=bin_size, color="black")
    ax4.set_xlabel("Seconds")

    plt.show()