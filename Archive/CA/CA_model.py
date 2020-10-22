import matplotlib
matplotlib.use("TkAgg")
from pylab import *
import math as m
import numpy as np
from CA import population

DENSE = 50000
SMALL = 12500
SPARSE = 12500
SMALL_SPARSE = 3125
ULTRA_SPARSE = 3125
NUM_ELECTRODES = 64
THRESHOLD = 100

class Neuron_model:
    def __init__(self, individual, initial_p = 0.01, n = int(m.ceil(m.sqrt(SMALL))), duration = 600, resolution = 10):
        self.n = n
        self.p = individual.genotype[0]
        self.neighbor_width = individual.genotype[1]
        self.spont_p = individual.genotype[2]
        self.reset_n = individual.genotype[3]
        self.initial_p = initial_p
        self.steps = duration*resolution
        self.duration = duration
        self.resolution = resolution

    def run_simulation(self):
        global config, nextconfig, step,spikes
        step = 0
        self.__initialize()
        while step < self.steps:
            self.__update()
            step += 1
        return spikes

    def __initialize(self):
        global config, nextconfig, step,spikes
        config = zeros([self.n,self.n])
        self.electrodes = self.__get_electrodes()
        for row in range(len(config)):
            for col in range(len(config[0])):
                config[row][col] = self.reset_n if random() < self.initial_p else 0
        nextconfig = config
        step = 0
        spikes = np.zeros(self.duration)

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
        spikes[int(step//self.resolution)] += self.__get_spikes()

    def __get_spikes(self):
        global config, nextconfig, step,spikes
        s = 0
        for el in self.electrodes:
            if config[el[0]][el[1]] == self.reset_n:
                s += 1
        return s


    def __get_electrodes(self):
        global config, nextconfig, step,spikes
        electrodes = []
        for row in range(len(config) // 9, len(config)-len(config) // 9, len(config) // 9):
            for col in range(len(config) // 9, len(config)-len(config) // 9, len(config) // 9):
                electrodes.append((row, col))
        if len(electrodes) != 64:
            raise Exception("Wrong number of electrodes")
        return electrodes


