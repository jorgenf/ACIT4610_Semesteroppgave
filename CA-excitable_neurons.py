import pycxsimulator
from pylab import *

width = 100
height = 100
initProb = 0.01
maxState = 12

cell_data = []

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

def observe():
    global config

    subplot(2, 1, 1)
    cla()
    imshow(config, vmin = 0, vmax = maxState, cmap = cm.binary)
    axis('image')
    title('t = ' + str(time))

    subplot(2, 1, 2)
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
