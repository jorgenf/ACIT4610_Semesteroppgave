from multiprocessing import Pool, current_process
from random import randint, random, choice, shuffle
import Population
import CellularAutomataModel
import Data
import Fitness
import NetworkModel


class Evolution:
    def __init__(self, parameters):
        self.model_type = parameters["MODEL_TYPE"][0]
        self.dimension = parameters["DIMENSION"]
        self.population_size = parameters["POPULATION_SIZE"]
        self.simulation_duration = parameters["SIMULATION_DURATION"]
        self.resolution = parameters["TIME_STEP_RESOLUTION"]
        self.reference_phenotype = parameters["REFERENCE_PHENOTYPE"]
        self.reference_spikes = Data.get_spikes_file(
            parameters["REFERENCE_PHENOTYPE"], 
            recording_len=self.simulation_duration
            )
        self.parents_p = parameters["PARENTS_P"]
        self.retained_adults_p = parameters["RETAINED_ADULTS_P"]
        self.mutation_p = parameters["MUTATION_P"]

    #Sorts the array of individuals by decreasing fitness. Returns the PARENTS_P-percentage best
    def select_parents(self, individuals):
        individuals.sort(key=lambda x: x.fitness, reverse=True)
        best_individuals = individuals[:round(len(individuals) * self.parents_p)]
        return best_individuals


    #Selects the RETAINED_ADULTS_P-percentage best and adds to return-list. Shuffles array, then matches two-and-two
    # individuals until return-list is full. If RETAINED_ADULTS_P is present then certain matches might occur more often
    def reproduce(self, individuals):
        individuals.sort(key=lambda x: x.fitness, reverse=True)
        retained_adults = individuals[:round(len(individuals) * self.retained_adults_p)]
        shuffle(individuals)
        next_generation = retained_adults if retained_adults else []
        i = 0
        while len(next_generation) < self.population_size:
            genes = []
            for gene1, gene2 in zip(individuals[i].genotype, individuals[i+1].genotype):
                genes.append(random() if random() < self.mutation_p else choice((gene1,gene2)))
            next_generation.append(Population.Individual(g_type=genes))
            i = (i + 2) % (len(individuals) - 1)
        return next_generation


    #Runs simulation and adds phenotype list to individual. Gets fitness score and adds to individual.
    def generate_phenotype(self, individual):
        # REFERENCE_PHENOTYPE = "Small - 7-1-35.spk.txt"
        print(current_process().name, end=" ")
        if self.model_type == "CA":
            # develop phenotype from genotype
            phenotype = CellularAutomataModel.CellularAutomataModel(
                individual = individual, 
                dimension = self.dimension, 
                duration= self.simulation_duration, 
                resolution = self.resolution
                ).run_simulation()

        elif self.model_type == "Network":
            phenotype = NetworkModel.NetworkModel(individual = individual, dimension = 30, duration = self.simulation_duration).run_simulation()
        burst_corr, avg_dist, fitness = Fitness.get_fitness_2(Data.get_spikes_pheno(phenotype, self.simulation_duration), self.reference_spikes)
        individual.phenotype = phenotype
        individual.fitness = fitness
        return individual

