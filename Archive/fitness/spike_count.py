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

    spikes = data_points["t"]

    # sort data by electrode ID
    data_by_electrode = [ [] for _ in range(64)]
    for row in data_points:
        data_by_electrode[row["electrode"]].append(row["t"])

    # convert to array
    spikes_per_array = np.array(data_by_electrode)

    # count average fire rate per electrode (spikes per second)
    spike_rates = {key:[] for key in range(64)}
    for key, item in enumerate(data_by_electrode):
        f_c = len(data_by_electrode[key]) / recording_len
        spike_rates[key] = f_c # spike rate
    spike_rate_per_array = np.array([*spike_rates.values()])

    f.close
    return (spikes, spikes_per_array, spike_rate_per_array)

def make_raster_plot(neural_data_filepath, simulation_data_filepath, simulation_length):
    import matplotlib.pyplot as plt
    import numpy as np

    neuron_spikes, neuron_spikes_per_array, _ = read_recording(
        neural_data_filepath, 
        recording_start=60*1, # starting point in seconds
        recording_len=simulation_length # simlation length in seconds, set to match simulation
        )

    sim_spikes, sim_spikes_per_array, _ = read_recording(simulation_data_filepath)

    # plot neural spikes
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
    ax1.eventplot(
        neuron_spikes_per_array,
        linewidths=0.5
        )
    ax1.set_xlabel("Seconds")
    ax1.set_ylabel("Electrode ID")
    ax1.set_title("Neural raster plot")
    
    # plot simulation spikes
    ax2.eventplot(
        sim_spikes_per_array,
        linewidths=0.5,
        color = "black"
        )
    ax2.set_xlabel("Seconds")
    ax2.set_title("Simulation raster plot")

    ax3.hist(neuron_spikes, bins=simulation_length)
    ax3.set_xlabel("Seconds")
    ax3.set_ylabel("Spikes per second")

    ax4.hist(sim_spikes, bins=simulation_length, color="black")
    ax4.set_xlabel("Seconds")

    plt.show()
    
if __name__ == "__main__":
    
    neural_data_filepath = r"Data\Dense - 2-1-20.spk.txt"
    simulation_data_filepath = r"CA_excitable\simulation_data.txt"

    make_raster_plot(neural_data_filepath, simulation_data_filepath, 120)