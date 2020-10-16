import pycxsimulator
import pylab
from pylab import *
from matplotlib import pyplot as plt
import networkx as nx

k = 4
dimension = 32
random_fire_prob = 0.1


def alter_state(neuron, inp):
   """
   Return the next state of a neuron.
   :param neuron: The neuron as the current node in the network.
   :param inp: This iteration's input to the current neuron.
   :return: Next state: 0 or 1.
   """
   #  Refractory period (simplified)
   if neuron['state'] == 1:
      return 0
   #  Firing threshold (simplified)
   elif inp >= 3:
      return 1
   #  Random firing probability
   elif random() < random_fire_prob:
      return 1
   else:
      return 0
      

def initialize():
   global g, next_g
   g = nx.grid_2d_graph(dimension, dimension)
   g.pos = {(x, y): (y, -x) for x, y in g.nodes()}
   for i in g.nodes:
      if random() < random_fire_prob:
         g.nodes[i]['state'] = 1
      else:
         g.nodes[i]['state'] = 0
   next_g = g.copy()
   next_g.pos = g.pos


def observe():
   global g, next_g
   cla()
   nx.draw(g, pos=g.pos, cmap=cm.get_cmap('binary_r'), vmin=0, vmax=1,
           node_color=[g.nodes[i]['state'] for i in g.nodes],
           with_labels=False, node_size=60)


def update():
   global g, next_g
   for i in g.nodes:
      count = g.nodes[i]['state']
      for j in g.neighbors(i):
         count += g.nodes[j]['state']
      next_g.nodes[i]['state'] = alter_state(g.nodes[i], count)

   g, next_g = next_g, g

pycxsimulator.GUI().start(func=[initialize, observe, update])
