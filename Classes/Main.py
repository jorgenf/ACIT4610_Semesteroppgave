import CellularAutomataModel, Population, Data, Fitness, Evolution, Summary
from multiprocessing import Pool, current_process
import os
import numpy as np
import matplotlib.pyplot as plt

evolution_parameters = {
    "MODEL_TYPE": (
        "CA",  # name of model
        6, # size of genome (number of parameters in genotype)
        ( # labels
            "Neighborhood width", 
            "Random fire probability", 
            "Refrractory period", 
            "Inhibitory neurons", 
            "Integration constant", 
            "Leak constant"
            )),
    # "MODEL_TYPE": ("Network", 8),
    #Number of individuals in the population
    "POPULATION_SIZE" : 2,
    #Number of generations to run. Each generation will run a number og simulations equal to POPULATION_SIZE
    "NUM_GENERATIONS": 1,
    #Simulation duration in seconds
    "SIMULATION_DURATION": 10,
    #Number of simulation iterations per second
    "TIME_STEP_RESOLUTION": 1,
    #Chance for mutation for each gene selection
    "MUTATION_P": 0.1,
    #Percentage of current population that will create offspring
    "PARENTS_P": 0.5,
    #Percentage of current population that will be included in next generation
    "RETAINED_ADULTS_P": 0.1,
    #Type of fitness function used. NOT IMPLEMENTED!
    "FITNESS_FUNCTION": "Normalized cross correlation",
    "REFERENCE_PHENOTYPE": "Small - 7-1-35.spk.txt"
}

if __name__ == '__main__':
#Creates threads of run_thread method. Pool-size = threads - 1. Each thread result is mapped to a variable that is
#returned when all processes are finished
    def run_threads(individuals):
        p = Pool(os.cpu_count()-1)
        new_individuals = p.map(evo.generate_phenotype, individuals)
        return new_individuals

#Creates population object with POPULATION_SIZE. Runs loop for NUM_GENERATIONS.
#Creates the set of genes that apply to this specific population
    pop = Population.Population(
        evolution_parameters["POPULATION_SIZE"], 
        evolution_parameters["MODEL_TYPE"][1]
        )

    evo = Evolution.Evolution(evolution_parameters)
    print("Running simulation...")
    fitness_trend = []
    average_fitness_trend = []
    parameter_trend = []
    for i in range(evolution_parameters["NUM_GENERATIONS"]):
        print("\nGeneration:", i)
        print("Workers: ", end="")
        pop_with_phenotypes = run_threads(pop.individuals)
        fitness_trend.append([i.fitness for i in pop_with_phenotypes])
        average_fitness_trend.append(sum([i.fitness for i in pop_with_phenotypes])/evolution_parameters["POPULATION_SIZE"])
        parameter_trend.append(np.sum([i.genotype for i in pop_with_phenotypes],0)/POPULATION_SIZE)
        if i < evolution_parameters["NUM_GENERATIONS"] - 1:
            parents = evo.select_parents(pop_with_phenotypes)
            new_gen = evo.reproduce(parents)
            pop.individuals = new_gen
            print()
        else:
            pop.individuals = pop_with_phenotypes
        
    # pop.individuals.sort(key=lambda x: x.fitness, reverse=True)
    # best_individual = pop.individuals[0]

    #   Exports output data
    #   Plots individual fitness trends

    #   Plots average fitness trend
    # avg_fit, ax_avg_fit = plt.subplots()
    # ax_avg_fit.plot(average_fitness_trend, label="Average fitness")
    # ax_avg_fit.plot(fitness_trend, linestyle="",marker=".", color="red", label="Individual fitness")
    # ax_avg_fit.set_title("Fitness trend")
    # ax_avg_fit.set_xlabel("Generation")
    # ax_avg_fit.set_ylabel("Fitness score")
    # avg_fit.savefig("Output/average_fitness_trend.png")

    # print(pop.individuals)
    summary = Summary.Summary(pop, evolution_parameters, fitness_trend)
    summary.raster_plot()
    summary.fitness_trend

    #   Plot best phenotype
    # raster_plot = Data.raster_plot(
    #     best_individual.phenotype, 
    #     Data.read_recording(
    #         REFERENCE_PHENOTYPE, 
    #         recording_len=SIMULATION_DURATION,
    #         recording_start=0 # where to start reading experimental data [s]
    #         ), 
    #     SIMULATION_DURATION
    # )
    # raster_plot.savefig("Output/Best_individual.png")


    #   Plot best phenotype
    # raster_plot = Data.raster_plot(
    #     best_individual.phenotype, 
    #     Data.read_recording(
    #         REFERENCE_PHENOTYPE, 
    #         recording_len=SIMULATION_DURATION,
    #         recording_start=0 # where to start reading experimental data [s]
    #         ), 
    #     SIMULATION_DURATION
    # )
    # raster_plot.savefig("Output/Best_individual" + str(best_individual.genotype) + str(best_individual.fitness) + ".png")
