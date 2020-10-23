import Model
from pylab import *
import matplotlib
from matplotlib import pyplot as plt
import networkx as nx
import math as m
import numpy as np

matplotlib.use("TkAgg")

#  Defaults
DENSE = 50000
SMALL = 12500
SPARSE = 12500
SMALL_SPARSE = 3125
ULTRA_SPARSE = 3125
NUM_ELECTRODES = 64
THRESHOLD = 100

DURATION = 12
RESOLUTION = 10
DIMENSION = int(m.ceil(m.sqrt(SMALL)))
ELECTRODE_DIMENSION = int(m.sqrt(NUM_ELECTRODES))
ELECTRODE_SPACING = DIMENSION // (ELECTRODE_DIMENSION + 1)
RESTING_POTENTIAL = 0.5
TYPE_DISTRIBUTION = 0.25
LEAK_RATIO = 0.1
INTEGRATION_RATIO = 0.25
RANDOM_FIRE_PROBABILITY = 0.005


def get_electrodes(dimension):
    electrodes = np.zeros((ELECTRODE_DIMENSION, ELECTRODE_DIMENSION, 2))
    r = 0
    f = 1 if dimension % 9 == 0 else 0
    for row in range(dimension // 9, dimension + f - (dimension // 9), dimension // 9):
        c = 0
        for col in range(dimension // 9, dimension + f - (dimension // 9), dimension // 9):
            if (r == 0 or r == 7) and (c == 0 or c == 7):
                c += 1
                continue
            else:
                electrodes[r, c, 0] = row
                electrodes[r, c, 1] = col
                c += 1
        r += 1
    el_list = [list(i) for sub in electrodes for i in sub if (i[0] != 0 and i[1] != 0)]
    return el_list


class NetworkModel:

    def __init__(self, duration=DURATION, resolution=RESOLUTION, dimension=DIMENSION, rest_pot=RESTING_POTENTIAL,
                 type_dist=TYPE_DISTRIBUTION, leak_ratio=LEAK_RATIO, integ_ratio=INTEGRATION_RATIO,
                 ran_fire_prob=RANDOM_FIRE_PROBABILITY):
        self.step = 0
        self.duration = duration
        self.resolution = resolution
        self.steps = self.duration * self.resolution
        self.dimension = dimension
        self.electrodes = get_electrodes(dimension)
        self.rest_pot = rest_pot
        self.type_dist = type_dist
        self.leak_ratio = leak_ratio
        self.integ_ratio = integ_ratio
        self.ran_fire_prob = ran_fire_prob
        #  Initialize Dataset
        self.spikes = []
        #  Initialize Network
        self.config = nx.grid_2d_graph(self.dimension, self.dimension)
        self.config.pos = {(x, y): (x, y) for x, y in self.config.nodes()}
        for i in self.config.nodes:
            self.config.nodes[i]['mem_pot'] = self.rest_pot
            # Inhibiting or exciting
            if random() < self.type_dist:
                self.config.nodes[i]['type'] = -1
            else:
                self.config.nodes[i]['type'] = 1
            #  Firing or not firing
            if random() < self.ran_fire_prob:
                self.config.nodes[i]['state'] = 1
            else:
                self.config.nodes[i]['state'] = 0
        #  Copy Network
        self.next_config = self.config.copy()
        self.next_config.pos = self.config.pos

    def alter_state(self, neuron, inp):
        #  Refractory period (simplified)
        if neuron['state'] == 1:
            return 0, self.rest_pot
        #  If the neuron reached the firing threshold last iteration,
        #  return firing state and membrane potential of 1
        elif neuron['mem_pot'] >= 1:
            return 1, 1
        #  Calculate membrane potential after leaking and integrating
        membrane_potential = neuron['mem_pot']
        leak_potential = ((membrane_potential - self.rest_pot) * self.leak_ratio)
        membrane_potential = membrane_potential - leak_potential
        integrate = 0
        if inp > 1:
            integrate = inp * (self.integ_ratio / (inp - 1))
        elif inp == 1:
            integrate = inp * self.integ_ratio
        membrane_potential = membrane_potential + integrate
        #  If the membrane potential isn't high enough to fire,
        #  there's still a chance to randomly fire
        if random() < self.ran_fire_prob:
            return 1, 1
        #  Return non-firing state and the current membrane potential.
        else:
            return 0, membrane_potential

    def update(self):
        for i in self.config.nodes:
            count = 0
            for j in self.config.neighbors(i):
                count += self.config.nodes[j]['state'] * self.config.nodes[j]['type']
            self.next_config.nodes[i]['state'], self.next_config.nodes[i]['mem_pot'] = self.alter_state(
                self.config.nodes[i], count
            )
        self.config, self.next_config = self.next_config, self.config
        self.spikes.append(self.__get_spikes())

    def run_simulation(self):
        while self.step < self.steps:
            self.update()
            self.step += 1
        return self.spikes

    '''def __get_spikes(self):
        spikes = np.zeros((int(m.sqrt(NUM_ELECTRODES)), int(m.sqrt(NUM_ELECTRODES))))
        sqr_size = self.dimension // m.sqrt(NUM_ELECTRODES)
        for x, y in self.config.nodes():
            spikes[int(x // sqr_size)][int(y // sqr_size)] += 1 if self.config.nodes[(x, y)]['state'] == 1 else 0
        return np.count_nonzero(spikes > 100)'''
    
    def __get_spikes(self):
        s = []
        for x, y in self.electrodes:
            if self.config.nodes[(x, y)]['state'] == 1:
                s.append((
                    # spike time
                    self.step / self.resolution,
                    # spike on electrode id
                    1 * (x // (ELECTRODE_SPACING + 1)) + 8 * (y // (ELECTRODE_SPACING + 1))
                ))
        return s if s else 0
