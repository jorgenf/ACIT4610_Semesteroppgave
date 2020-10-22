import matplotlib
matplotlib.use("TkAgg")
from pylab import *
from CA import data as d
import math as m
import numpy as np
from CA import fitness_functions as f

DENSE = 50000
SMALL = 12500
SPARSE = 12500
SMALL_SPARSE = 3125
ULTRA_SPARSE = 3125
NUM_ELECTRODES = 64
THRESHOLD = 100


class CA_neuron_model:
    def __init__(self, comparing_file = None, n = int(m.ceil(m.sqrt(SMALL))), p = 0.3,neighbor_width = 1,spont_p = 0.0001,reset_n = 20,initial_p = 0.01, steps = 3000):
        self.comparing_file = comparing_file
        self.n = n
        self.p = p
        self.neighbor_width = neighbor_width
        self.spont_p = spont_p
        self.reset_n = reset_n
        self.initial_p = initial_p
        self.steps = steps
        self.fr = d.get_firing_rate("Small - 7-1-35.spk.txt")[0:int(steps/10)]

    def run_simulation(self):
        global step
        step = 0
        self.__initialize()
        while step < self.steps:
            self.__update()
            step += 1

        avg_dist = f.average_distance(self.fr, spikes)
        fig, (p1,p2) = subplots(2,1)
        title("Average distance: " + avg_dist, y=2.2)
        p1.plot(spikes, "r-", linewidth=1)
        p2.plot(self.fr, "b-", linewidth=1)
        savefig("CA/plot_output/" + str(avg_dist) + "_" + str(self.n) + "_" + str(self.p) + "_" + str(self.neighbor_width) + "_" + str(self.spont_p) + "_" + str(self.reset_n) + "_" + ".png")
        close(fig)
        return self.fr,spikes,avg_dist

    def __initialize(self):
        global config, nextconfig, step,spikes
        config = zeros([self.n,self.n])
        for row in range(len(config)):
            for col in range(len(config[0])):
                config[row][col] = self.reset_n if random() < self.initial_p else 0
        nextconfig = config
        step = 0
        spikes = np.zeros(int(self.steps/10))

    def __update(self):
        global config, nextconfig,step,spikes
        for x in range(self.n):
            for y in range(self.n):
                if random() < self.spont_p and config[x,y] == 0:
                    nextconfig[x,y] = self.reset_n
                elif config[x,y] == 0:
                    count = 0
                    for dx in range(-self.neighbor_width , self.neighbor_width + 1):
                        for dy in range(-self.neighbor_width , self.neighbor_width + 1):
                            if 0 <= x + dx < self.n and 0 <= y + dy < self.n:
                                count += (config[(x + dx) % self.n, (y + dy) % self.n]//self.reset_n) if random() < self.p else 0
                    nextconfig[x,y] = self.reset_n if count >= 1 else config[x, y]
                elif config[x,y] > 0:
                    nextconfig[x,y] = config[x,y] - 1
        config = nextconfig
        spikes[int(step//10)] += self.__get_spikes()

    def __get_spikes(self):
        spikes = np.zeros((int(m.sqrt(NUM_ELECTRODES)),int(m.sqrt(NUM_ELECTRODES))))
        sqr_size = self.n // m.sqrt(NUM_ELECTRODES)
        global config
        for row in range(self.n):
            for col in range(self.n):
                spikes[int(row//sqr_size)][int(col//sqr_size)] += 1 if config[row][col] == self.reset_n else 0
        return np.count_nonzero(spikes > 100)

