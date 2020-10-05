import math as m
import matplotlib
matplotlib.use("TkAgg")
from pylab import *
import random
import numpy as np
import statistics as s



def get_average(list):
    return sum(list)/len(list)

def get_average_low(list):
    return sum(sorted(list)[0:20])/20

def get_average_high(list):
    return sum(sorted(list)[len(list)-20: len(list)])/20

def get_mean(list):
    return s.median(list)

def average_distance(list_a,list_b):
    a = sorted(list_a)
    b = sorted(list_b)
    dist = []
    for i,j in zip(a,b):
        dist.append(abs(i-j))
    return "{:.2f}".format(sum(dist)/len(dist))

def total_dist(list_a, list_b):
    return abs(sum(list_a)-sum(list_b))/len(list_a)

'''
arr1 = []
arr2 = []
arr3 = []
arr4 = []

for i in range(100):
    arr1.append(random.randint(0,100))
    arr2.append(random.randint(900, 1000))
    arr3.append(random.randint(0,1000))
    arr4.append(random.randint(0, 1000))

arr5 = arr1 + arr2
arr6 = arr3 + arr4

print(average_distance(arr5,arr6))

print(total_dist(arr5,arr6))

subplot(2,1,1)
plot(arr5)
subplot(2,1,2)
plot(arr6)
show()


print(arr1)
print(get_average(arr1))
print(get_average_low(arr1))
print(get_average_high(arr1))
print(get_mean(arr1))


arr = [arr4,arr3,arr2,arr1]

for a in arr:
    for b in arr:
        print("-----")
        print(a)
        print(b)
        print(abs(get_mean(a) - get_mean(b)))
        print(abs(get_average_high(a)-get_average_high(b)))
        print(abs(get_average_low(a)-get_average_low(b)))
        print(abs(get_average(a)-get_average(b)))
        print("---END---")


subplot(4,1,1)
plot(arr1)
subplot(4,1,2)
plot(arr2)
subplot(4,1,3)
plot(arr3)
subplot(4,1,4)
plot(arr4)
show()
'''
