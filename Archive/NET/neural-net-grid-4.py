import pycxsimulator
import pylab
from pylab import *
from matplotlib import pyplot as plt
import networkx as nx
import math

k = 4
dimension = 10
resting_potential = 0.5
type_distribution = 0.25
leak_ratio = 0.1
integration_ratio = 0.25
random_fire_prob = 0.005


def alter_state(neuron, inp):
   #  Refractory period (simplified)
   if neuron['state'] == 1:
      return 0, resting_potential
   #  If the neuron reached the firing threshold last iteration,
   #  return firing state and membrane potential of 1
   elif neuron['mem_pot'] >= 1:
      return 1, 1
   #  Calculate membrane potential after leaking and integrating
   membrane_potential = neuron['mem_pot']
   leak_potential = ((membrane_potential - resting_potential) * leak_ratio)
   membrane_potential = membrane_potential - leak_potential
   integrate = 0
   if inp > 1:
      integrate = inp * (integration_ratio / (inp - 1))
   elif inp == 1:
      integrate = inp * integration_ratio
   membrane_potential = membrane_potential + integrate
   #  If the membrane potential isn't high enough to fire,
   #  there's still a chance to randomly fire
   if random() < random_fire_prob:
      return 1, 1
   #  Return non-firing state and the current membrane potential.
   else:
      return 0, membrane_potential


def random_edges(recur):
   global g, next_g
   """
   Create a new random edge for each node in the network.
   :param recur: Amount of times to run loop.
   """
   #  Initialize Edge container
   new_edges = []
   while recur > 0:
      #  Iterate through the nodes
      for i in g.nodes:
         #  Loop-and-a-half
         while True:
            #  Choose another node to connect a new edge to (random position)
            node_choice = ((round(random()*(dimension-1))), (round(random()*(dimension-1))))
            #  Break loop-and-a-half if node choice is not among current neighbors
            if node_choice not in g.neighbors(i):
               break
         dx, dy = abs(i[0] - node_choice[0]), abs(i[1] - node_choice[1])
         weight = (((dimension - 1) * math.sqrt(2)) - math.sqrt(dx ^ 2 + dy ^ 2)) / ((dimension - 1) * math.sqrt(2))
         new_edges.append((i, node_choice, round(weight, 2)))
      recur -= 1
   return new_edges
  
      
def initialize():
   global g, next_g
   g = nx.grid_2d_graph(dimension, dimension)
   g.pos = {(x, y): (x, y) for x, y in g.nodes()}
   for i in g.edges:
      g.edges[i]['weight'] = 1
   g.add_weighted_edges_from(random_edges(2))
   for i in g.nodes:
      g.nodes[i]['mem_pot'] = resting_potential
      # Inhibiting or exciting
      if random() < type_distribution:
         g.nodes[i]['type'] = -1
      else:
         g.nodes[i]['type'] = 1
   #  Firing or not firing
      if random() < random_fire_prob:
         g.nodes[i]['state'] = 1
      else:
         g.nodes[i]['state'] = 0
      
   next_g = g.copy()
   next_g.pos = g.pos


def observe():
   global g, next_g
   cla()
   nx.draw(g, pos=g.pos, cmap=cm.get_cmap('binary_r'), vmin=0, vmax=0.5,
           node_color=[g.nodes[i]['state'] for i in g.nodes],
           with_labels=False, node_size=60)


def update():
   global g, next_g
   for i in g.nodes:
      count = 0
      for j in g.neighbors(i):
         #   Sum the neighboring neurons' states (0 or 1), type (-1 or 1) and the weight of the edge (~0-1)
         count += g.nodes[j]['state'] * g.nodes[j]['type'] * g.edges[i, j]['weight']
      next_g.nodes[i]['state'], next_g.nodes[i]['mem_pot'] = alter_state(g.nodes[i], count)
   g, next_g = next_g, g


pycxsimulator.GUI().start(func=[initialize, observe, update])
