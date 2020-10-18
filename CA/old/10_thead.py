import numpy as np
import random as rn
import time
from multiprocessing import Process


m = np.random.randint(0,2,(12000,6000))


def run_1():
    for i in range(6000):
        for j in range(0,1200):
            m[j,i] *= 2
def run_2():
    for i in range(6000):
        for j in range(1200,2400):
            m[j,i] *= 2
def run_3():
    for i in range(6000):
        for j in range(2400,3600):
            m[j,i] *= 2
def run_4():
    for i in range(6000):
        for j in range(3600,4800):
            m[j,i] *= 2
def run_5():
    for i in range(6000):
        for j in range(4800,6000):
            m[j,i] *= 2
def run_6():
    for i in range(6000):
        for j in range(6000,7200):
            m[j,i] *= 2
def run_7():
    for i in range(6000):
        for j in range(7200,8400):
            m[j,i] *= 2
def run_8():
    for i in range(6000):
        for j in range(8400,9600):
            m[j,i] *= 2
def run_9():
    for i in range(6000):
        for j in range(9600,10800):
            m[j,i] *= 2
def run_10():
    for i in range(6000):
        for j in range(10800,12000):
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
    p7 = Process(target=run_7)
    p7.start()
    p8 = Process(target=run_8)
    p8.start()
    p9 = Process(target=run_9)
    p9.start()
    p10 = Process(target=run_10)
    p10.start()

    while True:
        if p1.is_alive() or p2.is_alive() or p3.is_alive() or p4.is_alive() or p5.is_alive() or p6.is_alive() or p7.is_alive() or p8.is_alive() or p9.is_alive() or p10.is_alive():
            pass
        else:
            print("done")
            print(time.time_ns()-start)
            exit()

