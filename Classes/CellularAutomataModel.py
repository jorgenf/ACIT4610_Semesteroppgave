from . import Model
import matplotlib
matplotlib.use("TkAgg")
from pylab import *
import math as m
import numpy as np

DENSE = 50000
SMALL = 12500
SPARSE = 12500
SMALL_SPARSE = 3125
ULTRA_SPARSE = 3125


NUM_ELECTRODES = 64
DIMENSION = int(m.ceil(m.sqrt(SMALL)))
ELECTRODE_DIMENSION = int(m.sqrt(NUM_ELECTRODES))
ELECTRODE_SPACING = DIMENSION // (ELECTRODE_DIMENSION + 1)


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


class CellularAutomataModel():
    def __init__(self, DNA, initial_p = 0.01, dimension = int(m.ceil(m.sqrt(SMALL))), duration = 600, resolution = 10):
        self.step = 0
        self.dimension = dimension
        self.p = DNA.p
        self.neighbor_width = DNA.neighbour_width
        self.spont_p = DNA.spont_p
        self.reset_n = DNA.reset_n
        self.initial_p = initial_p
        self.steps = duration*resolution
        self.duration = duration
        self.resolution = resolution
        self.electrodes = get_electrodes(dimension)
        #  Initialize Dataset
        self.spikes = []

    def run_simulation(self):
        global step
        self.__initialize()
        while self.step < self.steps:
            self.__update()
            self.step += 1
        return self.spikes

    def __initialize(self):
        global config, nextconfig, step,spikes
        config = zeros([self.dimension, self.dimension])
        for row in range(len(config)):
            for col in range(len(config[0])):
                config[row][col] = self.reset_n if random() < self.initial_p else 0
        nextconfig = config
        step = 0

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
        self.spikes.append(self.__get_spikes())

    def __get_spikes(self):
        global config, nextconfig, step,spikes
        s = 0
        for x, y in self.electrodes:
            if config[x][y] == self.reset_n:
                s.append((
                    # spike time
                    self.step / self.resolution,
                    # spike on electrode id
                    1 * (x // (ELECTRODE_SPACING + 1)) + 8 * (y // (ELECTRODE_SPACING + 1))
                ))
        return s
