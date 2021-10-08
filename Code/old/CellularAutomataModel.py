import Population
from pylab import *
import numpy as np
from random import random
import time
#  Defaults
DURATION = 100
DIMENSION = 10
RESOLUTION = 50
INDIVIDUAL = Population.Individual([
	#  Neighbourhood width
	0.5,
	#  Chance to randomly fire
	0.3,
	#  Refractory period
	0.4,
	#  Percentage of inhibiting neurons
	0.1,
	#  Integrating constant
	0.5,
	#  Leak constant
	0.1
])


def test_class():
	"""
	Run the model/simulation with defaults and plot the results.
	"""
	from Summary import make_raster_plot

	# use model to generate a phenotype
	pop = Population.Population(1, 6)
	model = CellularAutomataModel()
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


class CellularAutomataModel:
	"""
	Creates a 2D Cellular Automaton using numpy arrays.
	The cells in the CA emulate the behaviour of neurons.
	The model iterates over itself and updates the nodes based on a set of rules.
	Takes an individual's genotype as input, and returns its phenotype.
	"""
	
	def __init__(self, individual=INDIVIDUAL, dimension=DIMENSION, duration=DURATION, resolution=RESOLUTION):
		#   The width of the neighborhood   0-3
		self.neighborhood_width = round(individual.genotype[0] * 3)
		#   Chance to randomly fire (0-20)/100000
		self.random_fire_prob = individual.genotype[1] * (20 / 100000)
		#   Refractory period: time to recharge after firing    0-10
		self.refractory_period = round(individual.genotype[2] * 10)
		#   The distribution of inhibiting and exciting neurons 0-0.1
		self.type_dist = individual.genotype[3] / 10
		#   Integrating constant 40-100
		self.integrate_constant = round(individual.genotype[4] * 60 + 40)
		#   Leak constant 0-30
		self.leak_constant = round(individual.genotype[5] * 30)
		#   How many iterations make up 1 second
		self.resolution = resolution
		self.max_membrane_potential = 100
		self.step = 0
		self.duration = duration
		self.dimension = dimension
		self.neighborhood_size = ((2 * self.neighborhood_width + 1) ** 2) - 1
		self.steps = self.duration * self.resolution
		self.electrodes = get_electrodes(dimension)
		#   Initialize Dataset
		self.spikes = []
		self.config = zeros([self.dimension, self.dimension, 3])
		#   Initialize CA
		for row in range(len(self.config)):
			for col in range(len(self.config[0])):
				#   Sets value of the neuron's membrane potential
				self.config[row, col, 0] = self.max_membrane_potential \
					if random() < self.random_fire_prob else 0
				#   Sets the max refractory value if neuron is excited.
				self.config[row, col, 1] = self.refractory_period \
					if self.config[row, col, 0] == self.max_membrane_potential else 0
				# Inhibiting or exciting neuron
				self.config[row, col, 2] = -1 if random() < self.type_dist else 1
		#   Copy CA
		self.next_config = self.config
	
	def update(self):
		"""
		Apply the ruleset to the current CA and update the next iteration.
		"""
		for x in range(self.dimension):
			for y in range(self.dimension):
				#   The neurons have a chance to randomly fire
				if random() < self.random_fire_prob and self.config[x, y, 1] == 0:
					self.next_config[x, y, 1] = self.refractory_period
					self.next_config[x, y, 0] = self.max_membrane_potential
				#   If the neuron did not randomly fire, and the state is 0
				elif self.config[x, y, 1] == 0:
					#   Loop through neighbors with edge-checks (without wrap-around)
					for dx in range(x - self.neighborhood_width
					                if x - self.neighborhood_width >= 0 else 0,
					                x + self.neighborhood_width + 1
					                if x + self.neighborhood_width + 1 <= self.dimension else self.dimension):
						for dy in range(y - self.neighborhood_width
						                if y - self.neighborhood_width >= 0 else 0,
						                y + self.neighborhood_width + 1
						                if y + self.neighborhood_width + 1 <= self.dimension else self.dimension):
							#  Integrate input from neighbors in the membrane potential
							self.next_config[x, y, 0] += self.config[dx, dy, 2] * self.integrate_constant \
								if self.config[dx, dy, 0] >= self.max_membrane_potential else 0
					#   If the neuron reached the firing threshold last iteration,
					#   the neuron is excited and the max refractory value is set
					if self.config[x, y, 0] >= self.max_membrane_potential:
						self.next_config[x, y, 0] = self.max_membrane_potential
						self.next_config[x, y, 1] = self.refractory_period
				#   If the neuron did not randomly fire, and the state is above 0
				else:
					#  Decrement the refractory value
					self.next_config[x, y, 1] -= 1 if self.config[x, y, 1] > 0 else 0
					#  Leak the membrane potential its above 0
					self.next_config[x, y, 0] -= self.leak_constant if self.config[x, y, 0] > 0 else 0
		#  Update the configuration for the next iteration
		self.config = self.next_config
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
		for el in self.electrodes:
			if self.config[el[0], el[1], 0] >= self.max_membrane_potential:
				s.append((0 + (self.step / self.resolution), self.electrodes.index(el)))
		return s if s else 0


#   Run the class test and print the result when the script is run standalone.
if __name__ == "__main__":
	test_class()
