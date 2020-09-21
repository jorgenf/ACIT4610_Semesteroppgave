import matplotlib
matplotlib.use("TkAgg")
from pylab import *

n = 123
p = - 0.05
neighbor_width = 2
spont_p = 0.0001
color_res = 20

def initialize():
    global config, nextconfig
    config = zeros([n,n])
    nextconfig = config

def observe():
    global config, nextconfig
    cla()
    imshow(config, vmin = 0, vmax = color_res, cmap = cm.binary)


def update():
    global config, nextconfig
    for x in range(n):
        for y in range(n):
            if random() < spont_p and config[x,y] == 0:
                nextconfig[x,y] = color_res
            elif config[x,y] == 0:
                count = 0
                for dx in range(-neighbor_width , neighbor_width + 1):
                    for dy in range(-neighbor_width , neighbor_width + 1):
                        count += config[(x + dx) % n, (y + dy) % n]
                nextconfig[x,y] = color_res if random() < count/(color_res*(pow(((neighbor_width*2)+1),2)-1)) + p else config[x,y]
            elif config[x,y] > 0:
                nextconfig[x,y] = config[x,y] - 1
    config = nextconfig

import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])