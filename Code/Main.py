import os
import time
from multiprocessing import Pool, current_process
import numpy as np
import matplotlib.pyplot as plt
import CellularAutomataModel, Population, Data, Fitness, Evolution, Summary
"""
PARAMETERS
"""
# TYPE parameter sets properties specific for each model type
TYPE = {
    # Set properties for CA model
    "CA": (
        #   Name of model
        "CA",
        #   Size of genome (number of parameters in genotype)
        7,
        #   Labels
        (
            "Firing threshold"
            "Random fire probability", 
            "Refractory period",
            "Inhibition percentage",
            "Leak constant",
            "Integration constant",
            "Density constant"
        )),
    # Set properties for network model
    "Network": (
        #   Name of model
        "Network",
        #   Size of genome (number of parameters in genotype)
        7,
        #   Labels
        (
            "Firing threshold",
            "Neighborhood width",
            "Random fire probability",
            "Refractory period",
            "Type distribution",
            "Leak ratio",
            "Integration ratio"
        ))
}
#   Set general parameters for the evolutionary algorithm
evolution_parameters = {
    #   Choose between CA and Network by commenting out the other.
    #"MODEL_TYPE": TYPE["CA"],
       "MODEL_TYPE": TYPE["Network"],
    # Size of one dimension in the array / grid / matrix
    "DIMENSION": 10,
    #   Number of individuals in the population
    "POPULATION_SIZE": 50,
    #   Number of generations to run.
    #   Each generation will run one simulation of the model for every individual in the population
    "NUM_GENERATIONS": 5,
    #   Simulation duration in seconds
    "SIMULATION_DURATION": 100,
    #   Number of simulation iterations per second
    "TIME_STEP_RESOLUTION": 40,
    #   The probability of mutation in any gene
    "MUTATION_P": 0.15,
    #   The percentage of the current population that will create offspring
    "PARENTS_P": 0.5,
    #   The percentage of the current population that will carry over to the next generation
    "RETAINED_ADULTS_P": 0.1,
    #   Name of the file of experimental data used as reference for the fitness function and raster plot
    "REFERENCE_PHENOTYPE": "Small - 7-1-35.spk.txt"
}
"""
PROGRAM
"""
if __name__ == "__main__":
    start_time = time.time()
    
    def run_threads(individuals):
        """
        Creates threads of run_thread method.
        Pool-size = threads - 1.
        Each thread result is mapped to a variable that is returned when all processes are finished
        """
        p = Pool(os.cpu_count()-1)
        new_individuals = p.map(evo.generate_phenotype, individuals)
        return new_individuals
    
    #   Creates population object with POPULATION_SIZE.
    #   Creates the set of genes that apply to this specific population
    pop = Population.Population(
        evolution_parameters["POPULATION_SIZE"], 
        evolution_parameters["MODEL_TYPE"][1]
        )
    # Creates Evolution object with parameters set 
    evo = Evolution.Evolution(evolution_parameters)
    # Initialize datasets
    fitness_trend = []
    average_fitness_trend = []
    parameter_trend = []
    # Start the evolution. Runs loop for NUM_GENERATIONS
    print("Running simulation...")
    for i in range(evolution_parameters["NUM_GENERATIONS"]):
        print("\nGeneration:", i)
        print("Workers: ", end="")
        #   Run the evolutionary algorithm on the population
        pop_with_phenotypes = run_threads(pop.individuals)
        #   Record data of the population
        fitness_trend.append([i.fitness for i in pop_with_phenotypes])
        average_fitness_trend.append(sum(
            [i.fitness for i in pop_with_phenotypes]
        )/evolution_parameters["POPULATION_SIZE"])
        parameter_trend.append(np.sum(
            [i.genotype for i in pop_with_phenotypes], 0)/evolution_parameters["POPULATION_SIZE"])
        # Sort the population in order to pick out the best fitness
        sorted_pop = pop_with_phenotypes
        sorted_pop.sort(key=lambda x: x.fitness, reverse=True)
        #   If there is no recorded best individual, choose the best one of this generation
        if not evo.best_individual_overall:
            evo.best_individual_overall = (i, sorted_pop[0])
        #   If the fitness of the best individual in this generation is better than the best recorded individual,
        #   let the new one take its place as the best.
        elif evo.best_individual_overall[1].fitness < sorted_pop[0].fitness:
            evo.best_individual_overall = (i, sorted_pop[0])
        #   Reproduction
        if i < evolution_parameters["NUM_GENERATIONS"] - 1:
            parents = evo.select_parents(pop_with_phenotypes)
            new_gen = evo.reproduce(parents, pop_with_phenotypes)
            pop.individuals = new_gen
            print()
        else:
            pop.individuals = pop_with_phenotypes

    #   Save the running time of the script
    end_time = time.time()
    total_time = end_time - start_time

    # Save a summary of the evolution
    summary = Summary.Summary(pop, evolution_parameters, evo)
    summary.raster_plot()
    summary.fitness_trend_plot((fitness_trend, average_fitness_trend))
    summary.parameter_trend_plot(parameter_trend)
    summary.average_distance_plot()
    summary.output_text(total_time)

