def read_recording(filename, recording_start=0, recording_len=30*60):
    from operator import itemgetter
    import numpy as np

    # cleaning data, making array
    f = open(filename, "r")
    data_points = [line.split(" ") for line in f]
    data_points = np.array(
        [(row[0].rstrip(), row[1].rstrip()) for row in data_points], 
        dtype=[("t", "float64"), ("electrode", "int64")])

    # edit to requested recording length
    start_index, stop_index = np.searchsorted(data_points["t"], [recording_start, recording_start+recording_len])
    data_points = data_points[start_index:stop_index]

    # sort data by electrode ID
    data_by_electrode = [ [] for _ in range(64)]
    for row in data_points:
        data_by_electrode[row["electrode"]].append(row["t"])

    # convert to array
    spike_array = np.array(data_by_electrode)

    # count average fire rate per electrode (spikes per second)
    spike_rates = {key:[] for key in range(64)}
    for key, item in enumerate(data_by_electrode):
        f_c = len(data_by_electrode[key]) / (30*60) # 30 min recording
        spike_rates[key] = f_c # spike rate
    spike_rates_array = np.array([*spike_rates.values()])

    f.close
    return (spike_array, spike_rates_array)


    
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    neural_data_filepath = r"Data\Dense - 2-1-20.spk.txt"
    simulation_data_filepath = r"CA_excitable\simulation_data.txt"

    neuron_spikes, neuron_spike_rates = read_recording(
        neural_data_filepath, 
        recording_start=60*1, # starting point in seconds
        recording_len=10 # simlation length in seconds, set to match simulation
        )

    sim_spikes, sim_spike_rates = read_recording(simulation_data_filepath)

    # plot neural spikes
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    ax1.eventplot(
        neuron_spikes,
        linewidths=0.5
        )
    ax1.set_xlabel("Seconds")
    ax1.set_ylabel("Electrode ID")
    ax1.set_title("Neural raster plot")
    
    # plot simulation spikes
    ax2.eventplot(
        sim_spikes,
        linewidths=0.5
        )
    ax2.set_xlabel("Seconds")
    ax2.set_title("Simulation raster plot")

    plt.show()