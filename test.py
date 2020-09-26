import matplotlib
matplotlib.use("TkAgg")
from pylab import *
import data as d
import math as m
import pycxsimulator

DENSE = 50000
SMALL = 12500
SPARSE = 12500
SMALL_SPARSE = 3125
ULTRA_SPARSE = 3125


def run_simulation(plot_name, comparing_file = None, n = int(m.sqrt(SMALL)), p = 0.3,neighbor_width = 1,spont_p = 0.0001,reset_n = 20,initial_exc_p = 0.01, steps = 1700, show_plot = True):

    def initialize():
        global config, nextconfig, step,spikes
        config = zeros([n,n])
        for row in range(len(config)):
            for col in range(len(config[0])):
                config[row][col] = reset_n if random() < initial_exc_p else 0
        nextconfig = config
        step = 0
        spikes = []

    def observe():
        global config, nextconfig, step, spikes
        if show_plot:
            subplot(3,1,1)
            cla()
            imshow(config, vmin = 0, vmax = reset_n, cmap = cm.binary)
            subplot(3,1,2)
            plot(spikes, "r-")
            subplot(3,1,3)
            if comparing_file != None:
                plot(d.get_firing_rate(comparing_file), "b-")

    def update():
        global config, nextconfig,step,spikes
        if step > steps:
            savefig("plot_output/"+plot_name+"png")
            exit()
        else:
            for x in range(n):
                for y in range(n):
                    if random() < spont_p and config[x,y] == 0:
                        nextconfig[x,y] = reset_n
                    elif config[x,y] == 0:
                        count = 0
                        for dx in range(-neighbor_width , neighbor_width + 1):
                            for dy in range(-neighbor_width , neighbor_width + 1):
                                if 0 <= x + dx < n and 0 <= y + dy < n:
                                    count += (config[(x + dx) % n, (y + dy) % n]//reset_n) if random() < p else 0
                        nextconfig[x,y] = reset_n if count >= 1 else config[x, y]
                    elif config[x,y] > 0:
                        nextconfig[x,y] = config[x,y] - 1
            config = nextconfig
            spikes.append(len(config[np.where(config == reset_n)]))
            step += 1

    if show_plot:
        pycxsimulator.GUI().start(func=[initialize, observe, update])
    else:
        step = 0
        initialize()
        while step < steps:
            update()
            step += 1
        subplot(3, 1, 1)
        cla()
        imshow(config, vmin=0, vmax=reset_n, cmap=cm.binary)
        subplot(3, 1, 2)
        plot(spikes, "r-")
        subplot(3, 1, 3)
        plot(d.get_firing_rate("Small - 7-1-35.spk.txt"), "b-")
        savefig("plot_output/"+plot_name+"png")
        cla()

