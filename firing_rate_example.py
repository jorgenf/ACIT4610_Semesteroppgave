import data as d
import math as m
import matplotlib
matplotlib.use("TkAgg")
from pylab import *

file = d.get_firing_rate("Dense - 2-1-35.spk.txt")







plot(file)
show()

