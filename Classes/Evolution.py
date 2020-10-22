import Population

#Model type, NOT IMPLEMENTED!
MODEL_TYPE = "CA"
#Number of individuals in the population
POPULATION_SIZE = 100
#Number of generations to run. Each generation will run a number og simulations equal to POPULATION_SIZE
NUM_GENERATIONS = 10
#Simulation duration in seconds
SIMULATION_DURATION = 300
#Number of simulation iterations per second
TIME_STEP_RESOLUTION = 10
#Chance for mutation for each gene selection
MUTATION_P = 0.1
#Percentage of current population that will create offspring
PARENTS_P = 0.5
#Percentage of current population that will be included in next generation
RETAINED_ADULTS_P = 0.1
#Type of fitness function used. NOT IMPLEMENTED!
FITNESS_FUNCTION = "Normalized cross correlation"

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
        gene_1 = randint(3, 11) / 10 if random() < MUTATION_P else choice([array_one[i].genotype[0], array_one[i + 1].genotype[0]])
        gene_2 = randint(1, 11) if random() < MUTATION_P else choice([array_one[i].genotype[1], array_one[i + 1].genotype[1]])
        gene_3 = randint(1,20) / 100000 if random() < MUTATION_P else choice([array_one[i].genotype[2], array_one[i + 1].genotype[2]])
        gene_4 = randint(1, 21) if random() < MUTATION_P else choice([array_one[i].genotype[3], array_one[i + 1].genotype[3]])
        next_generation.append(population.Individual(gene_1, gene_2, gene_3, gene_4))
        i = (i + 2) % (len(array_one) - 1)
    return next_generation


#Runs simulation and adds phenotype list to individual. Gets fitness score and adds to individual.
def run_thread(individual):
    print(current_process().name, end="  ")
    phenotype = CA_model.Neuron_model(individual, duration= SIMULATION_DURATION, resolution = TIME_STEP_RESOLUTION).run_simulation()
    fitness = fitness_functions.cross_correlation(phenotype, data.get_firing_rate("Small - 7-1-35.spk.txt"))
    individual.set_phenotype(phenotype)
    individual.set_fitness(fitness)
    return individual

if __name__ == '__main__':
#Creates threads of run_thread method. Pool-size = threads - 1. Each thread result is mapped to a variable that is
#returned when all processes are finished
    def generate_phenotypes(individuals):
        p = Pool(os.cpu_count()-1)
        new_individuals = p.map(run_thread, individuals)
        return new_individuals

#Creates population object with POPULATION_SIZE. Runs loop for NUM_GENERATIONS.
    pop = Population.Population(POPULATION_SIZE)
    print("Running simulation...")
    for i in range(NUM_GENERATIONS):
        print("\nGeneration:", i)
        print("Workers: ", end="")
        pop_with_phenotypes = generate_phenotypes(pop.get_individuals())
        parents = select_parents(pop_with_phenotypes)
        new_gen = reproduce(parents)
        pop.update_individuals(new_gen)
