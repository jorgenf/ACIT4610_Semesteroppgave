import Population
from pylab import *
import networkx as nx
import math as m
import numpy as np
import time
#   Defaults
DURATION = 120
DIMENSION = 10
RESOLUTION = 50
RESTING_POTENTIAL = 0.5
FIRING_THRESHOLD = 1
NEIGHBORHOOD_WIDTH = 1
RANDOM_FIRE_PROBABILITY = 0.005
REFRACTORY_PERIOD = 1
TYPE_DISTRIBUTION = 0.25
LEAK_RATIO = 0.1
INTEGRATION_RATIO = 0.25
INDIVIDUAL = Population.Individual([
	FIRING_THRESHOLD - 1,
	NEIGHBORHOOD_WIDTH / 2,
	RANDOM_FIRE_PROBABILITY / 0.01,
	REFRACTORY_PERIOD / 2,
	TYPE_DISTRIBUTION / 0.5,
	LEAK_RATIO / 0.2,
	INTEGRATION_RATIO / 0.5,
])


def test_class():
	"""
	Run the model/simulation with defaults and plot the results.
	"""
	from Data import read_recording
	# use model to generate a phenotype
	model = NetworkModel()
	s = time.time_ns()
	output = model.run_simulation()
	o = time.time_ns()
	print(o - s)
	# generate reference phenotype from experimental data
	reference_file = {
		"small": "../Resources/Small - 7-2-20.spk.txt",
		"dense": "../Resources/Dense - 2-1-20.spk.txt"
	}
	reference = read_recording(reference_file["small"], recording_len=DURATION)
	#  Compare model output with experimental data


def get_electrodes(dimension):
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


class NetworkModel:
	"""
	Creates a 2D grid network using NetworkX.
	The nodes in the network emulate the behaviour of neurons.
	The model iterates over itself and updates the nodes based on a set of rules.
	Takes an individual's genotype as input, and returns its phenotype.
	"""
	
	def __init__(self, individual=INDIVIDUAL, dimension=DIMENSION, duration=DURATION, resolution=RESOLUTION):
		#   Firing Threshold in the membrane (Default: 1) (Range: ~1-2)
		self.firing_threshold = individual.genotype[0] + 1
		#   Extra possible neighbour in the network (Default: 1) (Range: 2-10)
		self.neighborhood_width = round(individual.genotype[1] * 8) + 2
		#   Chance to randomly fire (Default: 0.005 (0.5%)) (Range: ~0-0.01)
		self.random_fire_prob = individual.genotype[2] * 0.01
		#   Refractory period: time to recharge after firing (Default: 1) (Range: ~0.3-1.3)
		#   Subtracts this constant from the membrane potential when a neuron fires.
		self.refractory_period = individual.genotype[3] + 0.3
		#   The distribution of inhibiting and exciting neurons (Default: 0.25) (Range: ~0-0.5)
		self.type_dist = individual.genotype[4] * 0.5
		#   By which ratio does the membrane potential passively move towards the
		#   resting potential every iteration. (Default: 0.1) (Range: ~0-0.2)
		self.leak_ratio = individual.genotype[5] * 0.2
		#   By which ratio does the input from the neighborhood integrate with the neuron
		#   (Default: 0.5) (Range: ~0-0.5)
		self.integ_ratio = individual.genotype[6] * 0.5
		#   Resting potential in the membrane (Default: 0.5)
		#   Currently not controlled by the algorithm
		self.rest_pot = RESTING_POTENTIAL
		self.step = 0
		self.duration = duration
		self.dimension = dimension
		#   How many iterations make up 1 second (Default: 50)
		self.resolution = resolution
		self.steps = self.duration * self.resolution
		self.electrodes = get_electrodes(dimension)
		#  Initialize Dataset
		self.spikes = []
		#  Initialize Network
		self.config = nx.grid_2d_graph(self.dimension, self.dimension)
		for i in self.config.edges:
			self.config.edges[i]['weight'] = 1
		#   Add random extra edges according to neighborhood width
		self.config.add_weighted_edges_from(self.random_edges(self.neighborhood_width))
		#   Position field can be used to invert coordinates for visualization
		#   self.config.pos = {(x, y): (x, y) for x, y in self.config.nodes()}
		for i in self.config.nodes:
			self.config.nodes[i]['mem_pot'] = self.rest_pot
			# Inhibiting or exciting
			if random() < self.type_dist:
				self.config.nodes[i]['type'] = -1
			else:
				self.config.nodes[i]['type'] = 1
			#  Firing or not firing
			if random() < self.random_fire_prob:
				self.config.nodes[i]['state'] = 1
			else:
				self.config.nodes[i]['state'] = 0
		#  Copy Network
		self.next_config = self.config.copy()
		#   Copy position field (currently not needed)
		#   self.next_config.pos = self.config.pos
	
	def alter_state(self, neuron, inp):
		"""
		Return new state and membrane potential for a node/neuron.
		"""
		#  Calculate membrane potential after leaking and integrating
		membrane_potential = neuron['mem_pot']
		leak_potential = ((membrane_potential - self.rest_pot) * self.leak_ratio)
		membrane_potential = membrane_potential - leak_potential
		integrate = 0
		if inp > 1:
			integrate = inp * (self.integ_ratio / (inp - 1))
		elif inp > 0:
			integrate = inp * self.integ_ratio
		membrane_potential = membrane_potential + integrate
		#  Refractory period (simplified)
		if neuron['state'] == 1:
			return 0, membrane_potential - self.refractory_period
		#   If the neuron reached the firing threshold last iteration,
		#   return firing state and membrane potential of 1
		elif neuron['mem_pot'] >= self.firing_threshold:
			return 1, membrane_potential
		#   If the membrane potential isn't high enough to fire,
		#   there's still a chance to randomly fire
		if random() < self.random_fire_prob:
			return 1, 1
		#   Return non-firing state and the current membrane potential.
		else:
			return 0, membrane_potential
	
	def random_edges(self, recur):
		"""
		Create a new random edge for each node in the network.
		:param recur: Amount of times to run loop.
		"""
		#  Initialize Edge container
		new_edges = []
		max_coordinate = self.dimension - 1
		max_distance = max_coordinate * m.sqrt(2)
		while recur > 0:
			#   Iterate through the nodes
			for i in self.config.nodes:
				#   Loop-and-a-half
				while True:
					#   Choose another node to connect a new edge to (random position)
					node_choice = ((round(random() * max_coordinate)), (round(random() * max_coordinate)))
					#   Break loop-and-a-half if node choice is not among current neighbors
					if node_choice not in self.config.neighbors(i):
						break
				#   Distance between the nodes/neurons in the axes
				dx, dy = abs(i[0] - node_choice[0]), abs(i[1] - node_choice[1])
				weight = (max_distance - m.sqrt((dx ^ 2) + (dy ^ 2))) / max_distance
				new_edges.append((i, node_choice, round(weight, 2)))
			recur -= 1
		return new_edges
	
	def print_weights(self):
		for n, nbrs_dict in self.config.adjacency():
			for nbr, e_attr in nbrs_dict.items():
				if "weight" in e_attr:
					print(e_attr)
	
	def update(self):
		"""
		Apply the ruleset to the current Network and update the next iteration.
		"""
		for i in self.config.nodes:
			count = 0
			for j in self.config.neighbors(i):
				#   Sum the neighboring neurons' states (0 or 1), type (-1 or 1) and the weight of the edge (~0-1)
				count += self.config.nodes[j]['state'] * \
							self.config.nodes[j]['type'] * \
							self.config.edges[i, j]['weight']
			self.next_config.nodes[i]['state'], self.next_config.nodes[i]['mem_pot'] = self.alter_state(
				self.config.nodes[i], count
			)
		#  Update the configuration for the next iteration
		self.config, self.next_config = self.next_config, self.config
		#  Get the spikes from this iteration and append them to the list of spikes if there were any
		current_spikes = self.get_spikes()
		if current_spikes:
			self.spikes += current_spikes
	
	def run_simulation(self):
		"""
		Simulation loop.
		Return: Numpy array with spikes on electrode ID's.
		"""
		while self.step < self.steps:
			self.update()
			self.step += 1
		#   Return phenotype
		return np.array(self.spikes, dtype=[("t", "float64"), ("electrode", "int64")])
	
	def get_spikes(self):
		"""
		Get spikes in the current iteration.
		Return: List with spikes on electrodes in the network.
		"""
		s = []
		for x, y in self.electrodes:
			if self.config.nodes[(x, y)]['state'] == 1:
				s.append((0 + (self.step / self.resolution), self.electrodes.index((x, y))))
		return s if s else 0


#   Run the class test and print the result when the script is run standalone.
if __name__ == "__main__":
	test_class()
