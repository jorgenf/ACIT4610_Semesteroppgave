def read_recording():
    from operator import itemgetter
    import numpy as np
    # example file
    filename = r"Data\Dense - 2-1-20.spk.txt"
    f = open(filename, "r")
    data_points = [line.split(" ") for line in f]
    
    # sort by electrode
    data_points.sort(key=itemgetter(1))

    # cleaning data
    data_points = [(float(row[0].rstrip()), int(row[1].rstrip())) for row in data_points]

    # sort data by electrode ID
    data_by_electrode = {i:[] for i in range(59+1)} # 59 electrodes in experiment, but both 0 and 59 is present?
    for row in data_points:
        data_by_electrode[row[1]].append(row[0])
    # create numpy array for matplotlib
    spike_array = np.array([np.array(x) for x in [*data_by_electrode.values()]])
    

    # count average fire rate per electrode (spikes per second)
    spike_rates = {key:[] for key in data_by_electrode}
    for key in data_by_electrode:
        f_c = len(data_by_electrode[key]) / (30*60) # 30 min recording
        spike_rates[key] = f_c # spike rate
    spike_rates_array = np.array([*spike_rates.values()])


    # for key in spike_rates:
    #     print(key, spike_rates[key])
    # spike_rate_all_electrodes = sum(spike_rates.values()) / len(spike_rates.values())
    # print("All: ", spike_rate_all_electrodes)

    f.close
    return (spike_array, spike_rates_array)


    
if __name__ == "__main__":
    spikes, spike_rates = read_recording()
    print(spikes[:3][:5])
    print(spike_rates[:3])