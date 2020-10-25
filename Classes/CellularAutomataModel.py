import matplotlib
matplotlib.use("TkAgg")
from pylab import *
import math as m
import numpy as np
# from Classes import Population
import Population
from random import random

DENSE = 50000
SMALL = 12500
SPARSE = 12500
SMALL_SPARSE = 3125
ULTRA_SPARSE = 3125



class CellularAutomataModel():
    def __init__(self, individual,  dimension = int(m.ceil(m.sqrt(SMALL))), duration = 600, resolution = 10):
        self.dimension = dimension
        self.p = individual.genotype[0]
        self.neighbor_width = int(individual.genotype[1])
        self.spont_p = individual.genotype[2]
        self.reset_n = individual.genotype[3]
        self.steps = duration*resolution
        self.duration = duration
        self.resolution = resolution
        self.electrodes = self.__get_electrodes(dimension)

    def run_simulation(self):
        global step
        step = 0
        self.__initialize()
        while step < self.steps:
            self.__update()
            step += 1
        return spikes

    def __initialize(self):
        global config, nextconfig, step,spikes
        config = zeros([self.dimension, self.dimension])
        for row in range(len(config)):
            for col in range(len(config[0])):
                config[row][col] = self.reset_n if random() < self.spont_p else 0
        nextconfig = config
        step = 0
        spikes = np.zeros(self.duration)

    def __update(self):
        global config, nextconfig,step,spikes
        for x in range(self.dimension):
            for y in range(self.dimension):
                if random() < self.spont_p and config[x,y] == 0:
                    nextconfig[x,y] = self.reset_n
                elif config[x,y] == 0:
                    count = 0
                    for dx in range(-self.neighbor_width , self.neighbor_width + 1):
                        for dy in range(-self.neighbor_width , self.neighbor_width + 1):
                            if 0 <= x + dx < self.dimension and 0 <= y + dy < self.dimension:
                                count += (config[(x + dx) % self.dimension, (y + dy) % self.dimension] // self.reset_n) if random() < self.p else 0
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

    def __get_electrodes(self, dimension):
        el_list = []
        r = 0
        f = 1 if dimension % 9 == 0 else 0
        for row in range(dimension // 9, dimension + f - (dimension // 9), dimension // 9):
            c = 0
            for col in range(dimension // 9, dimension + f - (dimension // 9), dimension // 9):
                if (r == 0 or r == 7) and (c == 0 or c == 7):
                    c += 1
                    continue
                else:
                    el_list.append((row,col))
                    c += 1
            r += 1
        return el_list

