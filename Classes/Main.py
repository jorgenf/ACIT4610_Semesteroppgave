import CellularAutomataModel, Population, Data, Fitness, Evolution
from multiprocessing import Pool, current_process
import os
import numpy as np
import matplotlib.pyplot as plt

#Model type, NOT IMPLEMENTED!
MODEL_TYPE = "CA"; GENES = 6; LABELS = ["Neighborhood width", "Random fire probability", "Refrractory period", "Inhibitory neurons", "Integration constant", "Leak constant"]
#MODEL_TYPE = "Network" ; GENES = 8; LABELS = ["Firing threshold", "Neighborhood width", "Random fire probability", "Refractory period", "Type distribution", "Resolution", "Leak ratio", "Integration ratio"]
#Number of individuals in the population
POPULATION_SIZE = 30
DIMENSION = 10
#Number of generations to run. Each generation will run a number og simulations equal to POPULATION_SIZE
NUM_GENERATIONS = 50
#Simulation duration in seconds
SIMULATION_DURATION = 100
#Number of simulation iterations per second
TIME_STEP_RESOLUTION = 50
#Chance for mutation for each gene selection
MUTATION_P = 0.1
#Percentage of current population that will create offspring
PARENTS_P = 0.5
#Percentage of current population that will be included in next generation
RETAINED_ADULTS_P = 0.1
#Type of fitness function used. NOT IMPLEMENTED!
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
    evo = Evolution.Evolution(MODEL_TYPE, POPULATION_SIZE, DIMENSION, SIMULATION_DURATION, TIME_STEP_RESOLUTION, REFERENCE_PHENOTYPE, PARENTS_P, RETAINED_ADULTS_P, MUTATION_P)
    print("Running simulation...")
    fitness_trend = []
    average_fitness_trend = []
    parameter_trend = []
    for i in range(NUM_GENERATIONS):
        print("\nGeneration:", i)
        print("Workers: ", end="")
        pop_with_phenotypes = run_threads(pop.individuals)
        fitness_trend.append([i.fitness for i in pop_with_phenotypes])
        average_fitness_trend.append(sum([i.fitness for i in pop_with_phenotypes])/POPULATION_SIZE)
        parameter_trend.append(np.sum([i.genotype for i in pop_with_phenotypes],0)/POPULATION_SIZE)
        if i < NUM_GENERATIONS - 1:
            parents = evo.select_parents(pop_with_phenotypes)
            new_gen = evo.reproduce(parents)
            pop.individuals = new_gen
            print()
        else:
            pop.individuals = pop_with_phenotypes
    pop.individuals.sort(key=lambda x: x.fitness, reverse=True)
    best_individual = pop.individuals[0]

    #   Exports output data
    #   Plots individual fitness trends

    #   Plots average fitness trend
    avg_fit, ax_avg_fit = plt.subplots()
    ax_avg_fit.plot(average_fitness_trend, label="Average fitness")
    ax_avg_fit.plot(fitness_trend, linestyle="",marker=".", color="red")
    ax_avg_fit.legend(loc="upper left")
    ax_avg_fit.set_title("Fitness trend")
    ax_avg_fit.set_xlabel("Generation")
    ax_avg_fit.set_ylabel("Fitness score")
    avg_fit.savefig("Output/Fitness_trend_" + str(MODEL_TYPE) + "_" + str(POPULATION_SIZE) + "_" + str(NUM_GENERATIONS) + "_" + str(SIMULATION_DURATION) + "_" + str(TIME_STEP_RESOLUTION) + "_" + str(MUTATION_P) + "_" + str(PARENTS_P) + "_" + str(RETAINED_ADULTS_P) + ".png")

    #   Plot parameter trend
    par, ax_par = plt.subplots()
    for param, label in zip(list(map(list, zip(*parameter_trend))), LABELS):
        ax_par.plot(param, label=label)
    #ax_par.plot(parameter_trend, label="Parameter")
    ax_par.legend(loc="upper left")
    ax_par.set_title("Parameter trend")
    ax_par.set_xlabel("Generation")
    ax_par.set_ylabel("Normalized genome value")
    par.savefig("Output/Parameter_trend.png")

    #   Plot best phenotype
    raster_plot = Data.raster_plot(
        best_individual.phenotype, 
        Data.read_recording(
            REFERENCE_PHENOTYPE, 
            recording_len=SIMULATION_DURATION,
            recording_start=0 # where to start reading experimental data [s]
            ), 
        SIMULATION_DURATION
    )
    raster_plot.savefig("Output/Best_individual" + str(best_individual.genotype) + str(best_individual.fitness) + ".png")
