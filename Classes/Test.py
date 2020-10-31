import numpy as np
import random
import pandas
import matplotlib.pyplot as plt
from scipy import signal
import math



y1 = np.array([random.randint(0,300) for i in range(100)], dtype=float)
y2 = np.array([random.randint(0,300) for i in range(100)], dtype=float)


def average_distance_plot(simulation, reference):
    simulation_s = sorted(simulation)
    reference_s = sorted(reference)[:len(simulation)]

    fig, ax = plt.subplots(2,sharex="all")
    ax[0].set_xlabel("Sorted time [s]")
    ax[0].set_ylabel("Spikes per second")
    ax[0].plot(simulation_s, 'b', label="Simulation")
    ax[0].plot(reference_s, 'black', label="Reference")
    ax[0].plot([abs(sim - ref) for ref, sim in zip(simulation_s, reference_s)], label="Difference")
    ax[0].legend()
    ax[0].fill_between(range(len(simulation_s)), simulation_s, reference_s, color='red', alpha=0.2, where=[_y2 < _y1 for _y2, _y1 in zip(simulation_s, reference_s)])
    ax[0].fill_between(range(len(simulation_s)), simulation_s, reference_s, color='green', alpha=0.2, where=[_y2 > _y1 for _y2, _y1 in zip(simulation_s, reference_s)])
    for i in range(0,len(simulation_s), int(len(simulation_s)/10)):
        ax[0].text(i, min(simulation_s[i],reference_s[i])-20, simulation_s[i] - reference_s[i])


    ax[1].set_xlabel("Time [s]")
    ax[1].set_ylabel("Spikes per second")
    ax[1].plot(simulation, 'b', label="Simulation")
    ax[1].plot(reference, 'black', label="Reference")
    ax[1].legend()
    ax[1].fill_between(range(len(simulation)), simulation, reference, color='red', alpha=0.2, where=[_y2 < _y1 for _y2, _y1 in zip(simulation, reference)])
    ax[1].fill_between(range(len(simulation)), simulation, reference, color='green', alpha=0.2, where=[_y2 > _y1 for _y2, _y1 in zip(simulation, reference)])
    fig.show()


average_distance_plot(y1,y2)

'''
a_bursts = len(signal.argrelextrema(x, np.greater, order=3)[0])
b_bursts = len(signal.argrelextrema(y, np.greater, order=3)[0])

print(a_bursts)
print(b_bursts)
burst_corr = (a_bursts-abs(a_bursts-b_bursts))/a_bursts


a = sorted(x)
b = sorted(y)
dist = []
for i, j in zip(a, b):
    dist.append(abs(i - j))
avg_dist = (100-sum(dist) / len(dist))/100

print("Burst_corr: ", burst_corr)
print("Avg-dist: ", avg_dist)
print("Fitness", (burst_corr+avg_dist)/2)


plt.subplot(2,1,1)
plt.plot(x)
plt.subplot(2,1,2)
plt.plot(y)
plt.show()
'''