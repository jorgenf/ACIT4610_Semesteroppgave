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
    pass
