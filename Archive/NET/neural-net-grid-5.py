import pycxsimulator
import pylab
from matplotlib.colors import LinearSegmentedColormap
from pylab import *
from matplotlib import pyplot as plt
import networkx as nx
import math
import numpy as np

k = 4
dimension = 20
resting_potential = 0.5
type_distribution = 0.25
refractory_period = 0.8
leak_ratio = 0.1
integration_ratio = 0.25
random_fire_prob = 0.005
colors = [(0.8, 0, 0.1, 0.9), (0.5, 0.5, 0.5, 0.5), (0, 0.8, 0.1, 0.9)]
cmap_name = 'my_list'
my_color_map = LinearSegmentedColormap.from_list(
        cmap_name, colors)


def alter_state(neuron, inp):
   
   #  Calculate membrane potential after leaking and integrating
   membrane_potential = neuron['mem_pot']
   leak_potential = ((membrane_potential - resting_potential) * leak_ratio)
   membrane_potential = membrane_potential - leak_potential
   integrate = 0
   if inp > 1:
      integrate = inp * (integration_ratio / (inp - 1))
   elif inp > 0:
      integrate = inp * integration_ratio
   membrane_potential = membrane_potential + integrate
   #  Refractory period (simplified)
   if neuron['state'] == 1:
      return 0, membrane_potential - refractory_period
   #  If the neuron reached the firing threshold last iteration,
   #  return firing state and membrane potential of 1
   elif neuron['mem_pot'] >= 1:
      return 1, membrane_potential
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
   max_coordinate = dimension - 1
   max_distance = max_coordinate * math.sqrt(2)
   while recur > 0:
      #  Iterate through the nodes
      for i in g.nodes:
         #  Loop-and-a-half
         while True:
            #  Choose another node to connect a new edge to (random position)
            node_choice = ((round(random()*max_coordinate)), (round(random()*max_coordinate)))
            #  Break loop-and-a-half if node choice is not among current neighbors
            if node_choice not in g.neighbors(i):
               break
         dx, dy = abs(i[0] - node_choice[0]), abs(i[1] - node_choice[1])
         weight = (max_distance - math.sqrt(dx ^ 2 + dy ^ 2)) / max_distance
         new_edges.append((i, node_choice, round(weight, 2)))
      recur -= 1
   return new_edges
  
      
def initialize():
   global g, next_g, strong_edge, weak_edge
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

   strong_edge = [(u, v) for (u, v, d) in g.edges(data=True) if d["weight"] > 0.8]
   weak_edge = [(u, v) for (u, v, d) in g.edges(data=True) if d["weight"] <= 0.8]
   
   next_g = g.copy()
   next_g.pos = g.pos


def observe():
   global g, next_g, strong_edge, weak_edge
   cla()
   nx.draw_networkx_nodes(g, pos=g.pos, cmap=my_color_map, vmin=-1, vmax=1,
           node_color=[(g.nodes[i]['state'] * g.nodes[i]['type']) for i in g.nodes],
           node_size=60)
   nx.draw_networkx_edges(g, g.pos, edgelist=strong_edge, width=1, alpha=0.67)
   nx.draw_networkx_edges(
      g, g.pos, edgelist=weak_edge, width=1, alpha=0.33, edge_color="gray", style="dashed"
   )
   

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
