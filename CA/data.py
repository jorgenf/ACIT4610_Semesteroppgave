#Method takes filename for data and number of decimal places for intervall e.g. 0 is per second, 1 is per 10th of a second etc.
def get_firing_rate(file_name, interval_decimal_places = 0):
    file = open("Data/"+file_name,"r")
    times = []
    nodes = []
    spikes = []
    for line in file:
        time, node = line.split(" ")
        times.append(time)
        nodes.append(node)
        spikes.append(int(float(time)*(10**interval_decimal_places)))
    firing_rate = []
    for n in spikes:
        if n >= len(firing_rate):
            firing_rate.append(1)
        else:
            firing_rate[n] += 1
    return(firing_rate)
