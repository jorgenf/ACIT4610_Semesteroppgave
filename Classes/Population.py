import numpy as np
from random import randint


class Population:
    """
    A population consists of a type of individual that has certain genetic composition. Each individual in a population
    has the same number of genes, and each gene is within a range specific to that gene.
    """
    def __init__(self, pop_size, genome):
        self.population_size = pop_size
        self.genome = genome
        self.individuals = self.__create_individuals()

    def __create_individuals(self):
        pop = []
        for individual in range(self.population_size):
            g = []
            for gene in self.genome:
                g.append(randint(gene.min,gene.max)/gene.fraction)
            ind = Individual(g)
            pop.append(ind)
        return pop


class Individual:
    """
    Individuals consist of a genotype and a phenotype.
    The genotype is the genetic encoding of the individual.
    The phenotype is the part of the individual that is tested in the environment.
    The fitness is a score or a result of a fitness function.
    """
    def __init__(self, g_type):
        self.genotype = g_type
        self.phenotype = None
        self.fitness = None


#FJERN DENNE!
class Gene:
    '''
    A gene has a range from min to max. This is used when a gene is mutated to limit the possible
    values. It is also used when creating a population of individuals.
    '''
    def __init__(self, min, max, fraction = 1):
        self.min = min
        self.max = max
        self.fraction = fraction
