import matplotlib
matplotlib.use("TkAgg")
from pylab import *


SPLIT = 2
MUTATION = 0.1

class Population:
    def __init__(self, num_genotypes=100):
        self.num_genotypes = num_genotypes
        self.genotypes = self.__initiate_genotypes(self.num_genotypes)

    def __initiate_genotypes(self, num_genotypes):
        genotypes = []
        for n in range(num_genotypes):
            while True:
                p = randint(3, 11) / 10
                neighbor_width = randint(1, 11)
                spont_p = randint(1, 20) / 100000
                reset_n = randint(1, 21)
                if genotypes:
                    exist = False
                    for genotype in genotypes:
                        if p == genotype.p and neighbor_width == genotype.neighbour_width and spont_p == genotype.spont_p and reset_n == genotype.reset_n:
                            exist = True
                    if not exist:
                        genotypes.append(genotype(p, neighbor_width, spont_p, reset_n))
                        break
                else:
                    genotypes.append(genotype(p, neighbor_width, spont_p, reset_n))
                    break
        return genotypes

    def get_genotypes(self):
        return self.genotypes

    def update_genotypes(self, genotypes):
        self.genotypes = genotypes

    def select_parents(self):
        self.genotypes.sort(key = lambda x : x.corr, reverse=True)
        best_genotypes = self.genotypes[:len(self.genotypes) // SPLIT]
        return best_genotypes

    def reproduce(self, best_genotypes):
        next_generation = []
        for genotype in range(len(self.genotypes)):
            next_generation.append(genotype(randint(3, 11) / 10 if random() < MUTATION else best_genotypes[randint(len(best_genotypes))].p, randint(1, 11) if random() < MUTATION else best_genotypes[randint(len(best_genotypes))].neighbour_width, randint(1, 20) / 100000 if random() < MUTATION else best_genotypes[randint(len(best_genotypes))].spont_p, randint(1, 21) if random() < MUTATION else best_genotypes[randint(len(best_genotypes))].reset_n))
        self.genotypes = next_generation


class genotype:
    def __init__(self, p, neighbour_width, spont_p, reset_n):
        self.p = p
        self.neighbour_width = neighbour_width
        self.spont_p = spont_p
        self.reset_n = reset_n

    def set_fitness(self, fitness):
        self.fitness = fitness

    def get_fitness(self):
        return self.fitness

    def set_phenotype(self, phenotype):
        self.phenotype = phenotype

    def get_phenotype(self):
        return self.phenotype
