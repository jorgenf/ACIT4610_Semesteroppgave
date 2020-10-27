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
DURATION = 600
DIMENSION = int(m.ceil(m.sqrt(SMALL)))
INDIVIDUAL = Population.Individual([
    0.5,
    0.5,
    0.5,
    0.5,
    0.5,
    0.4
])


def test_class():
    """
    Run the model/simulation with defaults and return the output.
    """
    neural_ca = CellularAutomataModel()
    return neural_ca.run_simulation()


def get_electrodes(dimension):
    """
    Return a list of electrode positions based on the size of the network.
    The index of an electrode can be used as its ID.
    """
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


class CellularAutomataModel:
    """
    Creates a 2D Cellular Automaton using numpy arrays.
    The cells in the CA emulate the behaviour of neurons.
    The model iterates over itself and updates the nodes based on a set of rules.
    Takes an individual's genotype as input, and returns its phenotype.
    """
    def __init__(self, individual=INDIVIDUAL,  dimension=DIMENSION, duration=DURATION):
        #   Firing Threshold in the membrane    0-0.5
        self.firing_threshold = individual.genotype[0] / 2
        #   The width of the neighborhood   1-11
        self.neighborhood_width = round(individual.genotype[1] * 11)
        #   Chance to randomly fire (1-20)/100000
        self.random_fire_prob = individual.genotype[2] * (20 / 100000)
        #   Refractory period: time to recharge after firing    1-21
        self.refractory_period = round(individual.genotype[3] * 21)
        #   The distribution of inhibiting and exciting neurons 0.01-0.1
        self.type_dist = individual.genotype[4] / 10
        #   How many iterations make up 1 second    1-20
        self.resolution = round(individual.genotype[5]*20)
        self.step = 0
        self.duration = duration
        self.dimension = dimension
        self.steps = self.duration * self.resolution
        self.electrodes = get_electrodes(dimension)
        #   Initialize Dataset
        self.spikes = []
        self.config = zeros([self.dimension, self.dimension, 2])
        #   Initialize CA
        for row in range(len(self.config)):
            for col in range(len(self.config[0])):
                self.config[row, col, 0] = self.refractory_period if random() < self.random_fire_prob else 0
                self.config[row, col, 1] = -1 if random() < self.type_dist else 1
        #   Copy CA
        self.next_config = self.config

    '''
    #   Moved to __init__()
    def __initialize(self):
        global config, nextconfig, step,spikes
        config = zeros([self.dimension, self.dimension, 2])
        for row in range(len(config)):
            for col in range(len(config[0])):
                config[row, col, 0] = self.refractory_period if random() < self.random_fire_prob else 0
                config[row, col, 1] = -1 if random() < self.type_dist else 1
        nextconfig = config
        step = 0
        spikes = []
        '''

    def update(self):
        """
        Apply the ruleset to the current CA and update the next iteration.
        """
        for x in range(self.dimension):
            for y in range(self.dimension):
                if random() < self.random_fire_prob and self.config[x, y, 0] == 0:
                    self.next_config[x, y, 0] = self.refractory_period
                elif self.config[x, y, 0] == 0:
                    count = 0
                    for dx in range(-self.neighborhood_width , self.neighborhood_width + 1):
                        for dy in range(-self.neighborhood_width , self.neighborhood_width + 1):
                            if 0 <= x + dx < self.dimension and 0 <= y + dy < self.dimension:
                                count += self.config[x + dx, y + dy, 1] \
                                    if self.config[x + dx, y + dy, 0] == self.refractory_period \
                                    else 0
                    self.next_config[x, y, 0] = self.refractory_period \
                        if count >= self.firing_threshold * (((2 * self.neighborhood_width + 1) ** 2) - 1) \
                        else self.config[x, y, 0]
                elif self.config[x, y, 0] > 0:
                    self.next_config[x, y, 0] = self.config[x, y, 0] - 1
        self.config = self.next_config
        current_spikes = self.get_spikes()
        if current_spikes:
            self.spikes += current_spikes
       
    def run_simulation(self):
        """
        Simulation loop.
        Return: Numpy array with spikes on electrode ID's.
        """
        while self.step < self.steps:
            self.update()
            self.step += 1
        #   Return phenotype
        return np.array(self.spikes, dtype=[("t", "float64"), ("electrode", "int64")])

    def get_spikes(self):
        """
        Get spikes in the current iteration.
        Return: List with spikes on electrodes in the network.
        """
        s = []
        for el in self.electrodes:
            if self.config[el[0], el[1], 0] == self.refractory_period:
                s.append((0+(step/self.resolution), self.electrodes.index(el)))
        return s if s else 0
    

#   Run the class test and print the result when the script is run standalone.
if __name__ == "__main__":
    from Data import raster_plot, read_recording

    # use model to generate a phenotype
    simulation_length = 10 # [s]
    pop = Population.Population(1, 6)
    model = CellularAutomataModel(pop.individuals[0], duration=simulation_length)
    output = model.run_simulation()

    # generate reference phenotype from experimental data
    reference_file = {
        "small": "../Resources/Small - 7-2-20.spk.txt",
        "dense": "../Resources/Dense - 2-1-20.spk.txt"
    }
    reference = read_recording(reference_file["small"], recording_len=simulation_length)

    # compare model output with experimental data
    raster_plot(output, reference, simulation_length)
