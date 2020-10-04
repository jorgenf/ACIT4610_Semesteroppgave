import numpy as np
import random as rn
import time
from multiprocessing import Process


m = np.random.randint(0,2,(12000,6000))


def run_1():
    for i in range(6000):
        for j in range(0,2000):
            m[j,i] *= 2
def run_2():
    for i in range(6000):
        for j in range(2000,4000):
            m[j,i] *= 2
def run_3():
    for i in range(6000):
        for j in range(4000,6000):
            m[j,i] *= 2
def run_4():
    for i in range(6000):
        for j in range(6000,8000):
            m[j,i] *= 2
def run_5():
    for i in range(6000):
        for j in range(8000,1000):
            m[j,i] *= 2
def run_6():
    for i in range(6000):
        for j in range(10000,12000):
            m[j,i] *= 2




if __name__=='__main__':
    start = time.time_ns()
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
    while True:
        if p1.is_alive() or p2.is_alive() or p3.is_alive() or p4.is_alive() or p5.is_alive() or p6.is_alive():
            pass
        else:
            print("done")
            print(m)
            print(time.time_ns()-start)
            exit()

