import CellularAutomataModel, Population, Data, Fitness, Evolution
from multiprocessing import Pool, current_process
import os
import time

#Model type, NOT IMPLEMENTED!
MODEL_TYPE = "CA"; GENES = 6
#MODEL_TYPE = "Network" ; GENES = 8
#Number of individuals in the population
POPULATION_SIZE = 10
#Number of generations to run. Each generation will run a number og simulations equal to POPULATION_SIZE
NUM_GENERATIONS = 2
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



if __name__ == '__main__':
#Creates threads of run_thread method. Pool-size = threads - 1. Each thread result is mapped to a variable that is
#returned when all processes are finished
    def run_threads(individuals):
        p = Pool(os.cpu_count()-1)
        new_individuals = p.map(evo.generate_phenotype, individuals)
        return new_individuals

#Creates population object with POPULATION_SIZE. Runs loop for NUM_GENERATIONS.
#Creates the set of genes that apply to this specific population
    pop = Population.Population(POPULATION_SIZE, GENES)
    evo = Evolution.Evolution(MODEL_TYPE, POPULATION_SIZE, SIMULATION_DURATION, REFERENCE_PHENOTYPE, PARENTS_P, RETAINED_ADULTS_P, MUTATION_P)
    print("Running simulation...")
    for i in range(NUM_GENERATIONS):
        print("\nGeneration:", i)
        print("Workers: ", end="")
        pop_with_phenotypes = run_threads(pop.individuals)
        parents = evo.select_parents(pop_with_phenotypes)
        new_gen = evo.reproduce(parents)
        pop.individuals = new_gen
        print()
    pop.individuals = run_threads(pop.individuals)
    pop.individuals.sort(key=lambda x: x.fitness, reverse=True)
    best_individual = pop.individuals[0]
    
    # plot best phenotype
    Data.raster_plot(
        best_individual.phenotype, 
        Data.read_recording(
            REFERENCE_PHENOTYPE, 
            recording_len=SIMULATION_DURATION,
            recording_start=0 # where to start reading experimental data [s]
            ), 
        SIMULATION_DURATION
    )