from matplotlib.pyplot import cla
from CA import CA_neuron_model_2 as c
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
    neighbor_width = randint(1, 11)
    p = randint(3, 11) / 10
    reset_n = randint(1, 21)
    dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                             spont_p=spont_p, reset_n=reset_n).run_simulation()
    inc = True
    # tester neightbor width
    while True:
        if inc:
            neighbor_width += 1
        else:
            neighbor_width -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            neighbor_width -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            neighbor_width += 1
            break
        else:
            dist = curr_dist
    # tester p
    while True:
        if inc:
            p += 1
        else:
            p -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            p -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            p += 1
            break
        else:
            dist = curr_dist
    # tester reset_n
    while True:
        if inc:
            reset_n += 1
        else:
            reset_n -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            reset_n -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            reset_n += 1
            break
        else:
            dist = curr_dist


def run_2():
    print("started second...")
    spont_p = 0.00004
    neighbor_width = randint(1,11)
    p = randint(3,11)/10
    reset_n = randint(1,21)
    dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p = p, neighbor_width=neighbor_width,spont_p=spont_p,reset_n=reset_n).run_simulation()
    inc = True
    # tester neightbor width
    while True:
        if inc:
            neighbor_width += 1
        else:
            neighbor_width -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            neighbor_width -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            neighbor_width += 1
            break
        else:
            dist = curr_dist
    # tester p
    while True:
        if inc:
            p += 1
        else:
            p -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            p -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            p += 1
            break
        else:
            dist = curr_dist
    # tester reset_n
    while True:
        if inc:
            reset_n += 1
        else:
            reset_n -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            reset_n -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            reset_n += 1
            break
        else:
            dist = curr_dist


def run_3():
    print("started third...")
    spont_p = 0.00006
    neighbor_width = randint(1, 11)
    p = randint(3, 11) / 10
    reset_n = randint(1, 21)
    dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                             spont_p=spont_p, reset_n=reset_n).run_simulation()
    inc = True
    # tester neightbor width
    while True:
        if inc:
            neighbor_width += 1
        else:
            neighbor_width -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            neighbor_width -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            neighbor_width += 1
            break
        else:
            dist = curr_dist
    # tester p
    while True:
        if inc:
            p += 1
        else:
            p -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            p -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            p += 1
            break
        else:
            dist = curr_dist
    # tester reset_n
    while True:
        if inc:
            reset_n += 1
        else:
            reset_n -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            reset_n -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            reset_n += 1
            break
        else:
            dist = curr_dist

def run_4():
    print("started fourth...")
    spont_p = 0.00008
    neighbor_width = randint(1, 11)
    p = randint(3, 11) / 10
    reset_n = randint(1, 21)
    dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                             spont_p=spont_p, reset_n=reset_n).run_simulation()
    inc = True
    # tester neightbor width
    while True:
        if inc:
            neighbor_width += 1
        else:
            neighbor_width -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            neighbor_width -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            neighbor_width += 1
            break
        else:
            dist = curr_dist
    # tester p
    while True:
        if inc:
            p += 1
        else:
            p -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            p -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            p += 1
            break
        else:
            dist = curr_dist
    # tester reset_n
    while True:
        if inc:
            reset_n += 1
        else:
            reset_n -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            reset_n -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            reset_n += 1
            break
        else:
            dist = curr_dist


def run_5():
    print("started fifth...")
    spont_p = 0.0001
    neighbor_width = randint(1, 11)
    p = randint(3, 11) / 10
    reset_n = randint(1, 21)
    dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                             spont_p=spont_p, reset_n=reset_n).run_simulation()
    inc = True
    # tester neightbor width
    while True:
        if inc:
            neighbor_width += 1
        else:
            neighbor_width -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            neighbor_width -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            neighbor_width += 1
            break
        else:
            dist = curr_dist
    # tester p
    while True:
        if inc:
            p += 1
        else:
            p -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            p -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            p += 1
            break
        else:
            dist = curr_dist
    # tester reset_n
    while True:
        if inc:
            reset_n += 1
        else:
            reset_n -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            reset_n -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            reset_n += 1
            break
        else:
            dist = curr_dist

def run_6():
    print("started sixth...")
    spont_p = 0.00012
    neighbor_width = randint(1, 11)
    p = randint(3, 11) / 10
    reset_n = randint(1, 21)
    dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                             spont_p=spont_p, reset_n=reset_n).run_simulation()
    inc = True
    # tester neightbor width
    while True:
        if inc:
            neighbor_width += 1
        else:
            neighbor_width -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            neighbor_width -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            neighbor_width += 1
            break
        else:
            dist = curr_dist
    # tester p
    while True:
        if inc:
            p += 1
        else:
            p -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            p -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            p += 1
            break
        else:
            dist = curr_dist
    # tester reset_n
    while True:
        if inc:
            reset_n += 1
        else:
            reset_n -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            reset_n -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            reset_n += 1
            break
        else:
            dist = curr_dist


def run_7():
    print("started seventh...")
    spont_p = 0.00014
    neighbor_width = randint(1, 11)
    p = randint(3, 11) / 10
    reset_n = randint(1, 21)
    dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                             spont_p=spont_p, reset_n=reset_n).run_simulation()
    inc = True
    # tester neightbor width
    while True:
        if inc:
            neighbor_width += 1
        else:
            neighbor_width -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            neighbor_width -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            neighbor_width += 1
            break
        else:
            dist = curr_dist
    # tester p
    while True:
        if inc:
            p += 1
        else:
            p -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            p -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            p += 1
            break
        else:
            dist = curr_dist
    # tester reset_n
    while True:
        if inc:
            reset_n += 1
        else:
            reset_n -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            reset_n -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            reset_n += 1
            break
        else:
            dist = curr_dist


def run_8():
    print("started eighth...")
    spont_p = 0.00016
    neighbor_width = randint(1, 11)
    p = randint(3, 11) / 10
    reset_n = randint(1, 21)
    dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                             spont_p=spont_p, reset_n=reset_n).run_simulation()
    inc = True
    # tester neightbor width
    while True:
        if inc:
            neighbor_width += 1
        else:
            neighbor_width -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            neighbor_width -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            neighbor_width += 1
            break
        else:
            dist = curr_dist
    # tester p
    while True:
        if inc:
            p += 1
        else:
            p -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            p -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            p += 1
            break
        else:
            dist = curr_dist
    # tester reset_n
    while True:
        if inc:
            reset_n += 1
        else:
            reset_n -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            reset_n -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            reset_n += 1
            break
        else:
            dist = curr_dist


def run_9():
    print("started ninth...")
    spont_p = 0.00018
    neighbor_width = randint(1, 11)
    p = randint(3, 11) / 10
    reset_n = randint(1, 21)
    dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                             spont_p=spont_p, reset_n=reset_n).run_simulation()
    inc = True
    # tester neightbor width
    while True:
        if inc:
            neighbor_width += 1
        else:
            neighbor_width -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            neighbor_width -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            neighbor_width += 1
            break
        else:
            dist = curr_dist
    # tester p
    while True:
        if inc:
            p += 1
        else:
            p -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            p -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            p += 1
            break
        else:
            dist = curr_dist
    # tester reset_n
    while True:
        if inc:
            reset_n += 1
        else:
            reset_n -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            reset_n -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            reset_n += 1
            break
        else:
            dist = curr_dist


def run_10():
    print("started tenth...")
    spont_p = 0.0002
    neighbor_width = randint(1, 11)
    p = randint(3, 11) / 10
    reset_n = randint(1, 21)
    dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                             spont_p=spont_p, reset_n=reset_n).run_simulation()
    inc = True
    # tester neightbor width
    while True:
        if inc:
            neighbor_width += 1
        else:
            neighbor_width -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            neighbor_width -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            neighbor_width += 1
            break
        else:
            dist = curr_dist
    # tester p
    while True:
        if inc:
            p += 1
        else:
            p -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            p -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            p += 1
            break
        else:
            dist = curr_dist
    # tester reset_n
    while True:
        if inc:
            reset_n += 1
        else:
            reset_n -= 1
        curr_dist = c.CA_neuron_model(comparing_file="Data/Small - 7-1-35.spk.txt", p=p, neighbor_width=neighbor_width,
                                      spont_p=spont_p, reset_n=reset_n).run_simulation()
        if curr_dist >= dist and inc:
            inc = False
            reset_n -= 1
        elif curr_dist >= dist and not inc:
            inc = True
            reset_n += 1
            break
        else:
            dist = curr_dist


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
