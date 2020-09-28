from operator import itemgetter

# example file
# filename = r"D:\OneDrive\Dokumenter\skole\ASIC\ACIT4410 Evo AI\semesteroppgave\git\Data\Dense - 2-1-20.spk.txt"
filename = r"C:\Users\weyhak\OneDrive - Bane NOR\Dokumenter\GitHub\ACIT4610_Semesteroppgave\Data\Dense - 2-1-20.spk.txt"
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

# count average fire rate per electrode (spikes per second)
spike_rates = {key:[] for key in data_by_electrode}
for key in data_by_electrode:
    f_c = len(data_by_electrode[key]) / (30*60) # 30 min recording
    spike_rates[key] = f_c # spike rate

for key in spike_rates:
    print(key, spike_rates[key])

spike_rate_all_electrodes = sum(spike_rates.values()) / len(spike_rates.values())
print("All: ", spike_rate_all_electrodes)

f.close