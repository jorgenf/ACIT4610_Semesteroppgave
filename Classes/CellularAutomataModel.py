import matplotlib
matplotlib.use("TkAgg")
from pylab import *
import math as m
import numpy as np
from random import random
# from Classes import Population
import Population # forklaring https://stackoverflow.com/questions/43728431/relative-imports-modulenotfounderror-no-module-named-x


DENSE = 50000
SMALL = 12500
SPARSE = 12500
SMALL_SPARSE = 3125
ULTRA_SPARSE = 3125


class CellularAutomataModel():
    def __init__(self, individual,  dimension = int(m.ceil(m.sqrt(SMALL))), duration = 600):

        #0-0.5
        self.sp_threshold = individual.genotype[0]/2
        #1-11
        self.neighborhood_width = round(individual.genotype[1] * 11)
        #(1-20)/100000
        self.spontanous_excitation = individual.genotype[2] * (20 / 100000)
        #1-21
        self.refractory_period = round(individual.genotype[3] * 21)
        #0.01-0.1
        self.inhibitory_neuron_p = individual.genotype[4] / 10
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
                config[row, col, 0] = self.refractory_period if random() < self.spontanous_excitation else 0
                config[row, col, 1] = -1 if random() < self.inhibitory_neuron_p else 1
        nextconfig = config
        step = 0
        spikes = []

    def __update(self):
        global config, nextconfig,step,spikes
        for x in range(self.dimension):
            for y in range(self.dimension):
                if random() < self.spontanous_excitation and config[x, y, 0] == 0:
                    nextconfig[x, y, 0] = self.refractory_period
                elif config[x, y, 0] == 0:
                    count = 0
                    for dx in range(-self.neighborhood_width , self.neighborhood_width + 1):
                        for dy in range(-self.neighborhood_width , self.neighborhood_width + 1):
                            if 0 <= x + dx < self.dimension and 0 <= y + dy < self.dimension:
                                count += config[x + dx, y + dy, 1] if config[x + dx, y + dy, 0] == self.refractory_period else 0
                    nextconfig[x, y, 0] = self.refractory_period if count >= self.sp_threshold * (((2 * self.neighborhood_width + 1) ** 2) - 1) else config[x, y, 0]
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
            if config[el[0],el[1],0] == self.refractory_period:
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


#   Run the class test and print the result when the script is run standalone.
if __name__ == "__main__":
    from Data import raster_plot, read_recording

    # use model to generate a phenotype
    pop = Population.Population(1, 6)
    model = CellularAutomataModel(pop.individuals[0], duration=10)
    output = model.run_simulation()

    # generate reference phenotype from experimental data
    reference_file = {
        "small": "../Resources/Small - 7-2-20.spk.txt",
        "dense": "../Resources/Dense - 2-1-20.spk.txt"
    }
    reference = read_recording(reference_file["small"], recording_len=DURATION)

    # compare model output with experimental data
    raster_plot(output, reference, DURATION)
    