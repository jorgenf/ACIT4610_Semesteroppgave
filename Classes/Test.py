import numpy as np
import random
import pandas
import matplotlib.pyplot as plt
from scipy import signal
import math



x = np.array([random.randint(0,300) for i in range(100)], dtype=float)
y = np.array([random.randint(0,300) for i in range(100)], dtype=float)

a_bursts = len(signal.argrelextrema(x, np.greater, order=3)[0])
b_bursts = len(signal.argrelextrema(y, np.greater, order=3)[0])

print(a_bursts)
print(b_bursts)
burst_corr = (a_bursts-abs(a_bursts-b_bursts))/a_bursts


a = sorted(x)
b = sorted(y)
dist = []
for i, j in zip(a, b):
    dist.append(abs(i - j))
avg_dist = (100-sum(dist) / len(dist))/100

print("Burst_corr: ", burst_corr)
print("Avg-dist: ", avg_dist)
print("Fitness", (burst_corr+avg_dist)/2)


plt.subplot(2,1,1)
plt.plot(x)
plt.subplot(2,1,2)
plt.plot(y)
plt.show()
