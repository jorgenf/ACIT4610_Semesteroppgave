import matplotlib
matplotlib.use("TkAgg")
from pylab import *
import math as m
import numpy as np
from random import random
from ACIT4610_Semesteroppgave.Classes import Population

DENSE = 50000
SMALL = 12500
SPARSE = 12500
SMALL_SPARSE = 3125
ULTRA_SPARSE = 3125



class CellularAutomataModel():
    def __init__(self, individual,  dimension = int(m.ceil(m.sqrt(SMALL))), duration = 600):

        #(3-11)/10
        self.sp_threshold = ((individual.genotype[0] * 8) + 3) / 10
        #1-11
        self.neighbor_width = round(individual.genotype[1]*11)
        #(1-20)/100000
        self.spont_p = individual.genotype[2] * (20/100000)
        #1-21
        self.refractory_p = round(individual.genotype[3] * 21)
        #0-0.5
        self.i_neuron = (individual.genotype[4]/2)
        #1-20
        self.resolution = round(individual.genotype[5]*20)
        self.dimension = dimension
        self.steps = duration*self.resolution
        self.duration = duration
        self.electrodes = self.__get_electrodes(dimension)

    def run_simulation(self):
        global step, spikes
        step = 0
        self.__initialize()
        while step < self.steps:
            self.__update()
            step += 1
        phenotype = np.array(spikes, dtype=[("t", "float64"), ("electrode", "int64")])
        return phenotype

    def __initialize(self):
        global config, nextconfig, step,spikes
        config = zeros([self.dimension, self.dimension, 2])
        for row in range(len(config)):
            for col in range(len(config[0])):
                config[row, col, 0] = self.refractory_p if random() < self.spont_p else 0
                config[row, col, 1] = -1 if random() < self.i_neuron else 1
        nextconfig = config
        step = 0
        spikes = []

    def __update(self):
        global config, nextconfig,step,spikes
        for x in range(self.dimension):
            for y in range(self.dimension):
                if random() < self.spont_p and config[x, y, 0] == 0:
                    nextconfig[x, y, 0] = self.refractory_p
                elif config[x, y, 0] == 0:
                    count = 0
                    for dx in range(-self.neighbor_width , self.neighbor_width + 1):
                        for dy in range(-self.neighbor_width , self.neighbor_width + 1):
                            if 0 <= x + dx < self.dimension and 0 <= y + dy < self.dimension:
                                count += 1 if config[dx,dy,0] < self.refractory_p else 0
                    nextconfig[x, y, 0] = self.refractory_p if count >= self.sp_threshold*(((2*self.neighbor_width+1)**2)-1) else config[x, y, 0]
                elif config[x, y, 0] > 0:
                    nextconfig[x, y, 0] = config[x, y, 0] - 1
        config = nextconfig
        s = self.__get_spikes()
        if s:
            spikes += s

    def __get_spikes(self):
        global config, nextconfig, step,spikes
        s = []
        for el in self.electrodes:
            if config[el[0],el[1],0] == self.refractory_p:
                s.append((0+(step/self.resolution), self.electrodes.index(el)))
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


i = Population.Individual([random(),random(),random(),random(),random(),0.1])
res = CellularAutomataModel(i,50,10).run_simulation()
print(res)
