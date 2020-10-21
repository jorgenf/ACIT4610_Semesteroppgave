import matplotlib
matplotlib.use("TkAgg")
from pylab import *
import evolution

SPLIT = 2
MUTATION = 0.1

class Population:
    def __init__(self, num_individuals):
        self.num_individuals = num_individuals
        self.individuals = self.__initiate_individuals(self.num_individuals)

    def __initiate_individuals(self, num_individuals):
        individuals = []
        for n in range(num_individuals):
            while True:
                p = randint(3, 11) / 10
                neighbor_width = randint(1, 11)
                spont_p = randint(1, 20) / 100000
                reset_n = randint(1, 21)
                if individuals:
                    exist = False
                    for i in individuals:
                        if p == i.genotype[0] and neighbor_width == i.genotype[1] and spont_p == i.genotype[2] and reset_n == i.genotype[3]:
                            exist = True
                    if not exist:
                        individuals.append(Individual(p, neighbor_width, spont_p, reset_n))
                        break
                else:
                    individuals.append(Individual(p, neighbor_width, spont_p, reset_n))
                    break
        return individuals

    def get_individuals(self):
        return self.individuals

    def update_individuals(self, individuals):
        self.individuals = individuals




class Individual:
    def __init__(self, p, neighbour_width, spont_p, reset_n):
        self.genotype = [p,neighbour_width,spont_p,reset_n]

    def set_phenotype(self, phenotype):
        self.phenotype = phenotype

    def get_phenotype(self):
        return self.phenotype

    def set_fitness(self, fitness):
        self.fitness = fitness

    def get_fitness(self):
        return self.fitness

