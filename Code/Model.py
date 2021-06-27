import Population
from pylab import *
import networkx as nx
import math as m
import numpy as np
import time
import itertools
import random


MODEL = "network"
DURATION = 100
DIMENSION = 20
RESOLUTION = 40
BIDIRECTIONAL = False
# E_L
RESTING_POTENTIAL = -50
FIRING_THRESHOLD = 30
NEIGHBORHOOD_WIDTH = 1
RANDOM_FIRE_PROBABILITY = 0.005
REFRACTORY_PERIOD = 1
# C_L
LEAK_CONSTANT = 0.1
# C_I
INTEGRATION_CONSTANT = 0.25
# t_m
TIME_CONSTANT = 0.1
DENSITY_CONSTANT = 2
INHIBITION_PERCENTAGE = 0.25
ACTION_POTENTIAL = 10


INDIVIDUAL = Population.Individual([
    FIRING_THRESHOLD - 1,
    RANDOM_FIRE_PROBABILITY / 0.01,
    REFRACTORY_PERIOD / 2,
    INHIBITION_PERCENTAGE,
    LEAK_CONSTANT / 0.2,
    INTEGRATION_CONSTANT / 0.5,
    TIME_CONSTANT,
    DENSITY_CONSTANT
])


def test_class():
    """
    Run the model/simulation with defaults and plot the results.
    """
    from Summary import make_raster_plot

    # use model to generate a phenotype
    model = Model()
    s = time.time()
    output = model.run_simulation()

    print(f"{time.time() - s:.2f} seconds")

    # generate reference phenotype from experimental data
    reference_file = {
        "small": "../Resources/Small - 7-1-35.spk.txt",
        "dense": "../Resources/Dense - 2-1-20.spk.txt"
    }

    #  Compare model output with experimental data
    make_raster_plot(reference_file["small"], output, DURATION)

class Model:
    """
    Creates a 2D grid network using NetworkX.
    The nodes in the network emulate the behaviour of neurons.
    The model iterates over itself and updates the nodes based on a set of rules.
    Takes an individual's genotype as input, and returns its phenotype.
    """

    def __init__(self, individual=INDIVIDUAL, model=MODEL, dimension=DIMENSION, duration=DURATION, resolution=RESOLUTION, bidirectional=BIDIRECTIONAL):
        #   Firing Threshold in the membrane (Default: 1) (Range: ~1-2)
        self.firing_threshold = individual.genotype[0] + 1
        #   Chance to randomly fire (Default: 0.005 (0.5%)) (Range: ~0-0.01)
        self.random_fire_prob = individual.genotype[1] * 0.01
        #   Refractory period: time to recharge after firing (Default: 1) (Range: ~0.3-1.3)
        #   Subtracts this constant from the membrane potential when a neuron fires.
        self.refractory_period = individual.genotype[2] + 0.3
        #   The distribution of inhibiting and exciting neurons. Inhibition constant determines likelyhood of a
        self.inhibition_percentage = individual.genotype[3]
        #   By which ratio does the membrane potential passively move towards the
        #   resting potential every iteration. (Default: 0.1) (Range: ~0-0.2)
        self.leak_constant = individual.genotype[4] * 0.2
        #   By which ratio does the input from the neighborhood integrate with the neuron
        #   (Default: 0.5) (Range: ~0-0.5)
        self.integ_constant = individual.genotype[5] * 0.5
        self.time_constant = individual.genotype[6]
        self.density_constant = individual.genotype[7]

        #   Resting potential in the membrane (Default: 0.5)
        #   Currently not controlled by the algorithm
        self.rest_pot = RESTING_POTENTIAL
        self.step = 0
        self.model = model
        self.duration = duration
        self.dimension = dimension
        #   How many iterations make up 1 second (Default: 50)
        self.resolution = resolution
        self.steps = self.duration * self.resolution
        self.electrodes = self.get_electrodes(dimension)
        #  Initialize Dataset
        self.spikes = []
        #  Initialize Network
        self.config = nx.DiGraph()
        self.create_nodes()
        self.node_list = list(self.config.nodes)
        if self.model == "network":
            for node in range(len(self.node_list)):
                self.create_random_connections(node)
        elif self.model == "ca":
            for node in self.config.nodes:
                self.create_grid_connections(node)
        else:
            raise Exception("Invalid model chosen...")


        #   Position field can be used to invert coordinates for visualization
        #   self.config.pos = {(x, y): (x, y) for x, y in self.config.nodes()}

        #  Copy Network
        self.next_config = self.config.copy()
    #   Copy position field (currently not needed)
    #   self.next_config.pos = self.config.pos

    def create_nodes(self):
        self.position = list(itertools.product(range(self.dimension), range(self.dimension)))
        for pos in self.position:
            self.config.add_node(pos)
        for node in self.config.nodes:
            self.config.nodes[node]['mem_pot'] = self.rest_pot
            if random.random() < self.random_fire_prob:
                self.config.nodes[node]['state'] = 1
                self.config.nodes[node]['refractory'] = REFRACTORY_PERIOD
            else:
                self.config.nodes[node]['state'] = 0
                self.config.nodes[node]['refractory'] = 0

    def create_random_connections(self, node):
        pos = self.node_list[node]
        for n in range(node + 1, len(self.node_list)):
            if random.random() > INHIBITION_PERCENTAGE:
                weight = 1
            else:
                weight = -1
            distance = m.sqrt(((pos[0] - self.node_list[n][0])**2) + ((pos[1] - self.node_list[n][1])**2))
            p = m.exp(-((distance/DENSITY_CONSTANT)**2))
            if p >= random.random():
                order = random.choice([(pos, self.node_list[n]), (self.node_list[n], pos)])
                self.config.add_edge(order[0], order[1], weight=weight)

    def create_grid_connections(self, node):
        for x in range(node[0] - 1, node[0] + 2):
            for y in range(node[1] - 1, node[1] + 2):
                if 0 <= x < self.dimension and 0 <= y < self.dimension and (x != node[0] or y != node[1]):
                    if random.random() > INHIBITION_PERCENTAGE:
                        weight = 1
                    else:
                        weight = -1
                    self.config.add_edge(node, (x,y), weight=weight)
                else:
                    continue

    def alter_state(self, neuron, inp):
        """
        Return new state and membrane potential for a node/neuron.
        """

        dV = TIME_CONSTANT * (LEAK_CONSTANT * (self.rest_pot - neuron['mem_pot']) + (INTEGRATION_CONSTANT * inp))
        membrane_potential = neuron["mem_pot"] + dV
        if membrane_potential >= FIRING_THRESHOLD or random.random() < self.random_fire_prob:
            return 1, self.rest_pot, REFRACTORY_PERIOD
        else:
            return 0, membrane_potential, max(neuron["refractory"] - 1, 0)

    def update(self):
        """
        Apply the ruleset to the current Network and update the next iteration.
        """

        for node in self.config.nodes:
            in_potential = 0
            if self.config.nodes[node]["refractory"] == 0:
                neighbor_list = self.config.in_edges(node, data=True)
                for conn in neighbor_list:
                    state = self.config.nodes[conn[0]]["state"]
                    weight = conn[2]["weight"]
                    in_potential += state * weight * ACTION_POTENTIAL
                self.next_config.nodes[node]['state'], self.next_config.nodes[node]['mem_pot'],  self.next_config.nodes[node]["refractory"] = self.alter_state(self.config.nodes[node], in_potential)
            else:
                self.next_config.nodes[node]['state'], self.next_config.nodes[node]['mem_pot'], self.next_config.nodes[node]["refractory"] = self.alter_state(self.config.nodes[node], in_potential)

        #  Update the configuration for the next iteration
        self.config, self.next_config = self.next_config, self.config
        #  Get the spikes from this iteration and append them to the list of spikes if there were any
        current_spikes = self.get_spikes()
        if current_spikes:
            self.spikes += current_spikes

    def get_spikes(self):
        """
        Get spikes in the current iteration.
        Return: List with spikes on electrodes in the network.
        """
        s = []
        for x, y in self.electrodes:
            if any(node for node in self.config.nodes(data=True) if self.config[node]["position"]==(x,y) and self.config[node]["state"] == 1):
                s.append((0 + (self.step / self.resolution), self.electrodes.index((x, y))))
        return s if s else 0

    def get_electrodes(self, dimension):
        """
    	Return a list of electrode positions based on the size of the network.
    	The index of an electrode can be used as its ID.
    	"""
        el_list = []
        r = 0
        f = 1 if dimension % 9 == 0 else 0
        for row in range(dimension // 9, dimension + f - (dimension // 9), dimension // 9):
            c = 0
            for col in range(dimension // 9, dimension + f - (dimension // 9), dimension // 9):
                if (r == 0 or r == 7) and (c == 0 or c == 7):
                    c += 1
                    continue
                else:
                    el_list.append((row, col))
                    c += 1
            r += 1
        return el_list

    def print_weights(self):
        for n, nbrs_dict in self.config.adjacency():
            for nbr, e_attr in nbrs_dict.items():
                if "weight" in e_attr:
                    print(e_attr)

    def show_network(self, grid=False):
        edge_colors = []
        for e in self.config.edges(data=True):
            if e[2]["weight"] == 1:
                edge_colors.append("green")
            else:
                edge_colors.append("red")
        node_colors = []
        for n in self.config.nodes(data=True):
            if n[1]["state"] == 1:
                node_colors.append("blue")
            else:
                node_colors.append("black")
        if grid:
            p = {}
            for pos, node in zip(self.position, self.config.nodes):
                p[node] = pos
            nx.draw(self.config, p, edge_color=edge_colors, node_color=node_colors, node_size=50, width=0.5)
        else:
            nx.draw(self.config, edge_color=edge_colors, node_color=node_colors, node_size=50, width=0.5)
        plt.show()

    def run_simulation(self, plot=False):
        """
        Simulation loop.
        Return: Numpy array with spikes on electrode ID's.
        """
        while self.step < self.steps:
            self.update()
            self.step += 1
        self.show_network(grid=True)
        #   Return phenotype
        return np.array(self.spikes, dtype=[("t", "float64"), ("electrode", "int64")])


#   Run the class test and print the result when the script is run standalone.
if __name__ == "__main__":
    test_class()


