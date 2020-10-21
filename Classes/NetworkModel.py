from . import Model
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
RESTING_POTENTIAL = 0.5
TYPE_DISTRIBUTION = 0.25
LEAK_RATIO = 0.1
INTEGRATION_RATIO = 0.25
RANDOM_FIRE_PROBABILITY = 0.005


class NetworkModel(Model):

    def __init__(self, duration=DURATION, resolution=RESOLUTION, dimension=DIMENSION, rest_pot=RESTING_POTENTIAL,
                 type_dist=TYPE_DISTRIBUTION, leak_ratio=LEAK_RATIO, integ_ratio=INTEGRATION_RATIO,
                 ran_fire_prob=RANDOM_FIRE_PROBABILITY):
        self.step = 0
        self.duration = duration
        self.resolution = resolution
        self.steps = self.duration * self.resolution
        self.dimension = dimension
        self.rest_pot = rest_pot
        self.type_dist = type_dist
        self.leak_ratio = leak_ratio
        self.integ_ratio = integ_ratio
        self.ran_fire_prob = ran_fire_prob
        #  Initialize Dataset
        self.spikes = np.zeros(self.duration)
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
        self.spikes[int(self.step // self.resolution)] += self.__get_spikes()

    def run_simulation(self):
        while self.step < self.steps:
            self.update()
            self.step += 1
        return self.spikes

    def __get_spikes(self):
        spikes = np.zeros((int(m.sqrt(NUM_ELECTRODES)), int(m.sqrt(NUM_ELECTRODES))))
        sqr_size = self.dimension // m.sqrt(NUM_ELECTRODES)
        for x, y in self.config.nodes():
            spikes[int(x // sqr_size)][int(y // sqr_size)] += 1 if self.config.nodes[(x, y)]['state'] == 1 else 0
        return np.count_nonzero(spikes > 100)
