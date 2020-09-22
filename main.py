from matplotlib.pyplot import cla

import CA_neuron_model as c
import data as d
import numpy as np
from multiprocessing import Process

DENSE = 50000
SMALL = 12500
SPARSE = 12500
SMALL_SPARSE = 3125
ULTRA_SPARSE = 3125




def run_first():
    print("started first...")
    file_name = 0
    p = 0
    for neighbor_width in np.arange(1,10,3):
        for spont_p in np.arange(0.00001,0.0001,0.00003):
            for reset_n in np.arange(1,21,3):
                c.run_simulation("first_file" + str(file_name),comparing_file="Small - 7-1-35.spk.txt", show_plot=False,p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                file_name += 1
                cla()

def run_second():
    print("started second...")
    file_name = 0
    p = 0.2
    for neighbor_width in np.arange(1,10,3):
        for spont_p in np.arange(0.00001,0.0001,0.00003):
            for reset_n in np.arange(1,21,3):
                c.run_simulation("second_file" + str(file_name),comparing_file="Small - 7-1-35.spk.txt", show_plot=False,p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                file_name += 1
                cla()

def run_third():
    print("started third...")
    file_name = 0
    p = 0.4
    for neighbor_width in np.arange(1,10,3):
        for spont_p in np.arange(0.00001,0.0001,0.00003):
            for reset_n in np.arange(1,21,3):
                c.run_simulation("third_file" + str(file_name),comparing_file="Small - 7-1-35.spk.txt", show_plot=False,p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                file_name += 1
                cla()

def run_fourth():
    print("started fourth...")
    file_name = 0
    p = 0.6
    for neighbor_width in np.arange(1,10,3):
        for spont_p in np.arange(0.00001,0.0001,0.00003):
            for reset_n in np.arange(1,21,3):
                c.run_simulation("fourth_file" + str(file_name),comparing_file="Small - 7-1-35.spk.txt", show_plot=False,p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                file_name += 1
                cla()

def run_fifth():
    print("started fifth...")
    file_name = 0
    p = 0.8
    for neighbor_width in np.arange(1,10,3):
        for spont_p in np.arange(0.00001,0.0001,0.00003):
            for reset_n in np.arange(1,21,3):
                c.run_simulation("fifth_file" + str(file_name),comparing_file="Small - 7-1-35.spk.txt", show_plot=False,p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                file_name += 1
                cla()


def run_sixth():
    print("started sixth...")
    file_name = 0
    p = 1
    for neighbor_width in np.arange(1,10,3):
        for spont_p in np.arange(0.00001,0.0001,0.00003):
            for reset_n in np.arange(1,21,3):
                c.run_simulation("sixth_file" + str(file_name),comparing_file="Small - 7-1-35.spk.txt", show_plot=False,p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                file_name += 1
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