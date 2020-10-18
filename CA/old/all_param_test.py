from matplotlib.pyplot import cla
from CA import CA_neuron_model as c
import numpy as np
from multiprocessing import Process
from CA import data as d
import matplotlib
matplotlib.use("TkAgg")
from pylab import *
import random
import time

DENSE = 50000
SMALL = 12500
SPARSE = 12500
SMALL_SPARSE = 3125
ULTRA_SPARSE = 3125


def run_1():
    print("started first...")
    spont_p = 0.00002
    for neighbor_width in np.arange(1,10,3):
        for p in np.arange(0.3,1):
            for reset_n in np.arange(1,21,3):
                ca = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                ca.run_simulation()
                cla()


def run_2():
    print("started second...")
    spont_p = 0.00004
    for neighbor_width in np.arange(1,10,3):
        for p in np.arange(0.3,1):
            for reset_n in np.arange(1,21,3):
                ca = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                ca.run_simulation()
                cla()


def run_3():
    print("started third...")
    spont_p = 0.00006
    for neighbor_width in np.arange(1,10,3):
        for p in np.arange(0.3,1):
            for reset_n in np.arange(1,21,3):
                ca = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                ca.run_simulation()
                cla()


def run_4():
    print("started fourth...")
    spont_p = 0.00008
    for neighbor_width in np.arange(1,10,3):
        for p in np.arange(0.3,1):
            for reset_n in np.arange(1,21,3):
                ca = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                ca.run_simulation()
                cla()


def run_5():
    print("started fifth...")
    spont_p = 0.0001
    for neighbor_width in np.arange(1,10,3):
        for p in np.arange(0.3,1):
            for reset_n in np.arange(1,21,3):
                ca = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                ca.run_simulation()
                cla()


def run_6():
    print("started sixth...")
    spont_p = 0.00012
    for neighbor_width in np.arange(1,10,3):
        for p in np.arange(0.3,1):
            for reset_n in np.arange(1,21,3):
                ca = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                ca.run_simulation()
                cla()


def run_7():
    print("started seventh...")
    spont_p = 0.00014
    for neighbor_width in np.arange(1,10,3):
        for p in np.arange(0.3,1):
            for reset_n in np.arange(1,21,3):
                ca = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                ca.run_simulation()
                cla()


def run_8():
    print("started eighth...")
    spont_p = 0.00016
    for neighbor_width in np.arange(1,10,3):
        for p in np.arange(0.3,1):
            for reset_n in np.arange(1,21,3):
                ca = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                ca.run_simulation()
                cla()


def run_9():
    print("started ninth...")
    spont_p = 0.00018
    for neighbor_width in np.arange(1,10,3):
        for p in np.arange(0.3,1):
            for reset_n in np.arange(1,21,3):
                ca = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                ca.run_simulation()
                cla()


def run_10():
    print("started tenth...")
    spont_p = 0.0002
    for neighbor_width in np.arange(1,10,3):
        for p in np.arange(0.3,1):
            for reset_n in np.arange(1,21,3):
                ca = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n)
                ca.run_simulation()
                cla()


if __name__=='__main__':
    p1 = Process(target=run_1)
    p1.start()
    p2 = Process(target=run_2)
    p2.start()
    p3 = Process(target=run_3)
    p3.start()
    p4 = Process(target=run_4)
    p4.start()
    p5 = Process(target=run_5)
    p5.start()
    p6 = Process(target=run_6)
    p6.start()
    p7 = Process(target=run_7)
    p7.start()
    p8 = Process(target=run_8)
    p8.start()
    p9 = Process(target=run_9)
    p9.start()
    p10 = Process(target=run_10)
    p10.start()
