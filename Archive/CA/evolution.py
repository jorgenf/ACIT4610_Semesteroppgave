from random import randint, random, choice, shuffle
from CA import population



class Evolution:
    def __init__(self, mutation_p, surviving_parents_p, retained_adults_p):
        self.__mutation_p = mutation_p
        self.__surviving_parents_p = surviving_parents_p
        #elitism
        self.__retained_adults_p = retained_adults_p


    def get_next_generation(self, individuals):
        self.pop_size = len(individuals)
        parents = self.__select_parents(individuals)
        return self.__reproduce(parents)


    def __select_parents(self, individuals):
        individuals.sort(key=lambda x: x.fitness, reverse=True)
        self.retained_adults = individuals[:round(len(individuals) * self.__retained_adults_p)]
        best_individuals = individuals[:round(len(individuals) * self.__surviving_parents_p)]
        return best_individuals


    def __reproduce(self, individuals):
        shuffle(individuals)
        next_generation = self.retained_adults if self.retained_adults else []
        i = 0
        while len(next_generation) < self.pop_size:
            next_generation.append(population.Individual(randint(3, 11) / 10 if random() < self.__mutation_p else choice([individuals[i].genotype[0], individuals[i + 1].genotype[0]]), randint(1, 11) if random() < self.__mutation_p else choice([individuals[i].genotype[1], individuals[i + 1].genotype[1]]), randint(1, 20) / 100000 if random() < self.__mutation_p else choice([individuals[i].genotype[2], individuals[i + 1].genotype[2]]), randint(1, 21) if random() < self.__mutation_p else choice([individuals[i].genotype[3], individuals[i + 1].genotype[3]])))
            i = (i + 2) % (len(individuals)-1)
        return next_generation



