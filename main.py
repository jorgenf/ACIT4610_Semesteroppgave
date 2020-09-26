from matplotlib.pyplot import cla
import CA_neuron_model as c
import numpy as np
from multiprocessing import Process

DENSE = 50000
SMALL = 12500
SPARSE = 12500
SMALL_SPARSE = 3125
ULTRA_SPARSE = 3125


max_corr = []
best_spikes = []


def run_first():
    print("started first...")
    p = 0
    for neighbor_width in np.arange(1,10,3):
        for spont_p in np.arange(0.00001,0.0001,0.00003):
            for reset_n in np.arange(1,21,3):
                ca = c.CA_neuron_model(comparing_file="Small - 7-1-35.spk.txt", p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                ca.run_simulation()
                cla()

def run_second():
    print("started second...")
    p = 0.2
    for neighbor_width in np.arange(1,10,3):
        for spont_p in np.arange(0.00001,0.0001,0.00003):
            for reset_n in np.arange(1,21,3):
                ca = c.CA_neuron_model(comparing_file="Small - 7-1-35.spk.txt", p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                ca.run_simulation()
                cla()

def run_third():
    print("started third...")
    p = 0.4
    for neighbor_width in np.arange(1,10,3):
        for spont_p in np.arange(0.00001,0.0001,0.00003):
            for reset_n in np.arange(1,21,3):
                ca = c.CA_neuron_model(comparing_file="Small - 7-1-35.spk.txt", p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                ca.run_simulation()
                cla()

def run_fourth():
    print("started fourth...")
    p = 0.6
    for neighbor_width in np.arange(1,10,3):
        for spont_p in np.arange(0.00001,0.0001,0.00003):
            for reset_n in np.arange(1,21,3):
                ca = c.CA_neuron_model(comparing_file="Small - 7-1-35.spk.txt", p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                ca.run_simulation()
                cla()

def run_fifth():
    print("started fifth...")
    p = 0.8
    for neighbor_width in np.arange(1,10,3):
        for spont_p in np.arange(0.00001,0.0001,0.00003):
            for reset_n in np.arange(1,21,3):
                ca = c.CA_neuron_model(comparing_file="Small - 7-1-35.spk.txt", p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                ca.run_simulation()
                cla()


def run_sixth():
    print("started sixth...")
    p = 1
    for neighbor_width in np.arange(1,10,3):
        for spont_p in np.arange(0.00001,0.0001,0.00003):
            for reset_n in np.arange(1,21,3):
                ca = c.CA_neuron_model(comparing_file="Small - 7-1-35.spk.txt", p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                ca.run_simulation()
                cla()

if __name__=='__main__':
    p1 = Process(target=run_first)
    p1.start()
    p2 = Process(target=run_second)
    p2.start()
    p3 = Process(target=run_third)
    p3.start()
    p4 = Process(target=run_fourth)
    p4.start()
    p5 = Process(target=run_fifth)
    p5.start()
    p6 = Process(target=run_sixth)
    p6.start()