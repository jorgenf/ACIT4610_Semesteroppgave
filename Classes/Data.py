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
    
    """
    import numpy as np

    time_coef = 1000 # bin width [ms]

    spikes = []
    start_time = int(phenotype[0]["t"])
    for timestamp in phenotype["t"]:
        spikes.append(int(
            float(timestamp) * (1000/time_coef)
            ))
    
    firing_rate = []
    for n in spikes:
        if n >= len(firing_rate) + start_time:
            firing_rate.append(1)
        else:
            firing_rate[n-start_time] += 1
    return np.array(firing_rate, dtype=np.float)
