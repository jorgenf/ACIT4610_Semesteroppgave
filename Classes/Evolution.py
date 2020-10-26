import CellularAutomataModel, Population, Data, Fitness
from random import randint, random, choice, shuffle
from multiprocessing import Pool, current_process
import os

#Model type, NOT IMPLEMENTED!
MODEL_TYPE = "CA"
#Number of individuals in the population
POPULATION_SIZE = 50

#Number of generations to run. Each generation will run a number og simulations equal to POPULATION_SIZE
NUM_GENERATIONS = 10
#Simulation duration in seconds
SIMULATION_DURATION = 10
#Number of simulation iterations per second
TIME_STEP_RESOLUTION = 1
#Chance for mutation for each gene selection
MUTATION_P = 0.1
#Percentage of current population that will create offspring
PARENTS_P = 0.5
#Percentage of current population that will be included in next generation
RETAINED_ADULTS_P = 0.1
#Type of fitness function used. NOT IMPLEMENTED!
FITNESS_FUNCTION = "Normalized cross correlation"
REFERENCE_PHENOTYPE = "Small - 7-1-35.spk.txt"
REFERENCE_SPIKES = Data.get_spikes_file(REFERENCE_PHENOTYPE)

#Sorts the array of individuals by decreasing fitness. Returns the PARENTS_P-percentage best
def select_parents(array_one):
    array_one.sort(key=lambda x: x.fitness, reverse=True)
    best_individuals = array_one[:round(len(array_one) * PARENTS_P)]
    return best_individuals


#Selects the RETAINED_ADULTS_P-percentage best and adds to return-list. Shuffles array, then matches two-and-two
# individuals until return-list is full. If RETAINED_ADULTS_P is present then certain matches might occur more often
def reproduce(array_one):
    array_one.sort(key=lambda x: x.fitness, reverse=True)
    retained_adults = array_one[:round(len(array_one) * RETAINED_ADULTS_P)]
    shuffle(array_one)
    next_generation = retained_adults if retained_adults else []
    i = 0
    while len(next_generation) < POPULATION_SIZE:
        genes = []
        for gene1, gene2 in zip(array_one[i].genotype, array_one[i+1].genotype):
            genes.append(random() if random() < MUTATION_P else choice(gene1,gene2))
        next_generation.append(Population.Individual(g_type=genes))
        i = (i + 2) % (len(array_one) - 1)
    return next_generation


#Runs simulation and adds phenotype list to individual. Gets fitness score and adds to individual.
def run_thread(individual):
    print(current_process().name, end="  ")
    phenotype = CellularAutomataModel.CellularAutomataModel(individual, dimension = 30, duration= SIMULATION_DURATION).run_simulation()
    print(phenotype)
    fitness = Fitness.get_fitness(Data.get_spikes_pheno(phenotype), REFERENCE_SPIKES)
    individual.phenotype = phenotype
    individual.fitness = fitness
    return individual

if __name__ == '__main__':
#Creates threads of run_thread method. Pool-size = threads - 1. Each thread result is mapped to a variable that is
#returned when all processes are finished
    def generate_phenotypes(individuals):
        p = Pool(os.cpu_count()-1)
        new_individuals = p.map(run_thread, individuals)
        return new_individuals

#Creates population object with POPULATION_SIZE. Runs loop for NUM_GENERATIONS.
#Creates the set of genes that apply to this specific population
    pop = Population.Population(POPULATION_SIZE, 6)

    print("Running simulation...")
    for i in range(NUM_GENERATIONS):
        print("\nGeneration:", i)
        print("Workers: ", end="")
        pop_with_phenotypes = generate_phenotypes(pop.individuals)
        parents = select_parents(pop_with_phenotypes)
        new_gen = reproduce(parents)
        pop.individuals = new_gen
