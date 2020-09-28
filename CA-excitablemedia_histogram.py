import matplotlib.pyplot as plt

import pycxsimulator
from pylab import *

# params for CA model
width = 64
height = width # want a square
initProb = 0.01
maxState = 12

# params for MEA
mea_width = 8
mea_height = mea_width
inactive_cells = ( # 59 electrodes in experiment. corners inactive + a ground node
    (0,0),
    (1, 0), # ground node
    (mea_width-1, 0),
    (mea_width-1, mea_height-1),
    (0, mea_height-1)
    )

cell_data = []
mea_data = zeros([mea_height, mea_width])

def initialize():
    global time, config, nextConfig
    
    time = 0

    config = zeros([height, width])
    for x in range(width):
        for y in range(height):
            if random() < initProb:
                state = maxState
            else:
                state = 0
            config[y, x] = state

    nextConfig = zeros([height, width])

    # make the inactive electrodes appear black
    for row, col in inactive_cells:
        mea_data[row][col] = maxState

def observe():
    global config

    subplot(2, 2, 1)
    cla()
    imshow(config, vmin = 0, vmax = maxState, cmap = cm.binary)
    axis('image')
    title('t = ' + str(time))

    subplot(2, 2, 2)
    cla()
    imshow(mea_data, vmin=0, vmax=maxState, cmap=cm.binary)
    axis('image')

    subplot(2, 2, 3)
    cla()
    plot(cell_data, label = 'exited')
    legend()

def update():
    global time, config, nextConfig

    exite_count = 0
    time += 1

    for x in range(width):
        for y in range(height):
            state = config[y, x]
            if state == 0:
                num = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if config[(y+dy)%height, (x+dx)%width] == maxState:
                            num += 1
                if random() * 3 < num:
                    state = maxState
                    exite_count += 1
                else:
                    state = 0
            else:
                state -= 1
            nextConfig[y, x] = state

    config, nextConfig = nextConfig, config
    cell_data.append(exite_count)
    exite_count = 0

pycxsimulator.GUI().start(func=[initialize, observe, update])
