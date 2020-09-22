import matplotlib
matplotlib.use("TkAgg")
from pylab import *


n = 120
p = 0.01
th = 3
nh = 1

def initialize():
    global config, nextconfig, step
    config = zeros([n,n])
    nextconfig = config
    step = 0
def observe():
    global config, nextconfig, step
    subplot(2, 1, 1)
    cla()
    imshow(config, vmin = 0, vmax = 5, cmap = cm.binary)
    subplot(2,1,2)
    plot(step,config.sum()/n**2,"ro")
    step += 1

def update():
    global config, nextconfig
    for x in range(n):
        for y in range(n):
            if config[x][y] == 0 and random() < p:
                nextconfig[x][y] = 5
            elif config[x][y] == 0:
                count = 0
                for dx in [-nh, nh]:
                    for dy in [-nh, nh]:
                        if 0 <= x + dx < n and 0 <= y + dy < n:
                            if config[(x + dx), (y + dy)] == 5:
                                count += 1
                if count > th:
                    nextconfig[x,y] = 5
            else:
                config[x][y] -= 1
    config = nextconfig
    print(config.sum())
import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])