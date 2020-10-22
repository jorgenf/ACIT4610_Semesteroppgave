from pylab import *
import matplotlib
from matplotlib import pyplot as plt
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


class Model:

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

    def update(self):
        pass

    def run_simulation(self):
        while self.step < self.steps:
            self.update()
            self.step += 1
        return self.spikes

    def __get_spikes(self):
        pass
