from operator import itemgetter


filename = r"D:\OneDrive\Dokumenter\skole\ASIC\ACIT4410 Evo AI\semesteroppgave\git\Data\Dense - 2-1-20.spk.txt"
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

# discard if no spikes on electrode
data_by_electrode = {key:data_by_electrode[key] for key in data_by_electrode if data_by_electrode[key]}

# implementation of burst detection algorithm
"""
Wagenaar et al 2005: MEABench: A toolset for multi-electrode data acquisition and on-line analysis

Let fc be the average firing rate on electrode c, that is, the
total number of spikes recorded on that electrode divided by the
duration of the recording. We then define threshold inter-spike
intervals (ISI), τc, for each electrode c. This τc is set to 1/(4fc) or to
100 ms, whichever is smaller. The factor four ensures that only
spikes that succeed each other faster than four times the average
firing rate can be considered burstlets.
"""
firing_rates = {key:[] for key in data_by_electrode}
for key in data_by_electrode:
    f_c = len(data_by_electrode[key]) / (30*60)
    tau_c = 1 / (4*f_c)
    if tau_c > .1:
        tau_c = .1
    firing_rates[key] = (f_c, tau_c)


"""
Initially, the algorithm considers each electrode independently. 
For a given electrode, it searches for sequences of four or
more spikes with all internal ISIs less than τc. 
"""

core_burstlets = {key:[] for key in data_by_electrode}
for key in data_by_electrode:
    sequence = 0
    for i, entry in enumerate(data_by_electrode[key][:-1]):
        t_delta = data_by_electrode[key][i+1] - data_by_electrode[key][i]
        if t_delta < firing_rates[key][1]:
            sequence += 1
        else:
            if sequence >= 4:
                core_burstlets[key].append((data_by_electrode[key][i-sequence], data_by_electrode[key][i])) # start/end
                sequence = 0

for key in core_burstlets:
    if key in range(10):
        print(key, core_burstlets[key][:5])
"""
After these ‘core’ burstlets have been found, they are extended into the past and
the future to also contain spikes that have ISIs less than 200 ms,
(or less than 1/(3fc) , whichever is smaller). Thus, a burstlet consists
of a core of at least four very closely spaced spikes, with an ‘entourage’
of any number of slightly less closely spaced spikes, all on one electrode.
"""

"""
Once all burstlets on all electrodes have been found, they are sorted in
temporal order. A burst is then simply a sequence of one or more burstlets
that have non-zero temporal overlap.
"""




"""
In many cases, a small number of electrodes record strongly
elevated firing rates for extended periods after a global burst,
sometimes until the next one. If that happens, several global
bursts would all be grouped together according to the algo
rithm as described so far. This problem is corrected in a post
processing stage. Each detected burst is considered in turn, and
a graph of the number of simultaneous burstlets vs. time is con
structed. If a putative burst corresponds to several global bursts,
this graph will have more than one hump. The algorithm finds
these humps, and splits the bursts accordingly.
"""



# print(firing_rates)
# for key in data_by_electrode:
#     print(key, data_by_electrode[key][:10])
# for line in (data_points[:10]):
#     print(line)
f.close