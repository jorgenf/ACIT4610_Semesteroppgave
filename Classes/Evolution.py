from multiprocessing import Pool, current_process
from random import randint, random, choice, shuffle
import Population
import CellularAutomataModel
import Data
import Fitness
import NetworkModel


class Evolution:
    def __init__(self, model_type, population_size, simulation_duration, resolution, reference_phenotype, parents_p, retained_adults_p, mutation_p):
        self.model_type = model_type
        self.population_size = population_size
        self.simulation_duration = simulation_duration
        self.resolution = resolution
        self.reference_phenotype = reference_phenotype
        self.reference_spikes = Data.get_spikes_file(reference_phenotype, recording_len=simulation_duration)
        self.parents_p = parents_p
        self.retained_adults_p = retained_adults_p
        self.mutation_p = mutation_p

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
        REFERENCE_PHENOTYPE = "Small - 7-1-35.spk.txt"
        print(current_process().name, end="  ")
        if self.model_type == "CA":
            phenotype = CellularAutomataModel.CellularAutomataModel(individual = individual, dimension = 30, duration= self.simulation_duration, resolution = self.resolution).run_simulation()
        elif self.model_type == "Network":
            phenotype = NetworkModel.NetworkModel(individual = individual, dimension = 30, duration = self.simulation_duration).run_simulation()
        fitness = Fitness.get_fitness_2(Data.get_spikes_pheno(phenotype, self.simulation_duration), self.reference_spikes)
        individual.phenotype = phenotype
        #plt = Data.raster_plot(individual.phenotype, Data.read_recording(REFERENCE_PHENOTYPE, recording_len=self.simulation_duration, recording_start=0),self.simulation_duration)
        #plt.savefig("Output/"+ str(fitness) + ".png")
        individual.fitness = fitness
        return individual

