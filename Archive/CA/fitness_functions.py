import math as m
import matplotlib
matplotlib.use("TkAgg")
from pylab import *
import numpy as np
from numpy.fft import fft, ifft


def average_distance(list_a,list_b):
    a = sorted(list_a)
    b = sorted(list_b)
    dist = []
    for i,j in zip(a,b):
        dist.append(abs(i-j))
    return "{:.2f}".format(sum(dist)/len(dist))


def cross_correlation(list_a, list_b, type = "full"):
    c = np.correlate(list_a, list_b, type)
    return max(c)


def convolve(list_a, list_b):
    return np.convolve(list_a, list_b)


def circular_cross_correlation(list_a, list_b):
        list_b = list_b[:len(list_a)]
        return max(ifft(fft(list_a) * fft(list_b).conj()).real)


def normalized_cross_correlation(list_a, list_b):
    return cross_correlation(list_a,list_b)/(cross_correlation(list_a,list_a, "same")*cross_correlation(list_b, list_b, "same"))


def normalized_circular_cross_correlation(list_a, list_b):
    return circular_cross_correlation(list_a, list_b)/(circular_cross_correlation(list_a, list_a)*circular_cross_correlation(list_b,list_b))