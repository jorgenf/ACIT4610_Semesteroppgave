import os
import time
import csv
import sys
import getopt
from multiprocessing import Pool

import numpy as np
import matplotlib.pyplot as plt
from tqdm.contrib.concurrent import process_map

from Model import Model
import Population, Evolution, Summary


"""
PARAMETERS

"""

# TYPE parameter sets properties specific for each model type
TYPE = {
    # Set properties for CA model
    "ca": (
        "ca",  # name of model
        7, # size of genome (number of parameters in genotype)
        ( # labels
            # "Resting potential",            # E_L
            "Firing threshold",
            "Random fire probability",
            # "Neighborhood width",
            "Inhibition percentage"
            "Refractory period",
            "Leak constant",                # C_L
            "Integration constant",         # C_I
            "Density constant"                 # t_m
            )),

    "network": (
        "network",  # name of model
        7, # size of genome (number of parameters in genotype)
        ( # labels
            # "Resting potential",            # E_L
            "Firing threshold",
            "Random fire probability",
            # "Neighborhood width",
            "Inhibition percentage"
            "Refractory period",
            "Leak constant",                # C_L
            "Integration constant",         # C_I
            "Density constant"                 # t_m
            )),
}


"""
FUNCTIONS

"""

# process the arguments given when running this script
def process_arguments():
    input_file = ""
    desired_workers = None
    help_string = f"{sys.argv[0]} -i <inputfile.csv>"

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:w:", ["input=", "workers="])
    except getopt.GetoptError:
        print(help_string)
        sys.exit(2)

    print(opts)
    for opt, arg in opts:
        if opt == "-h":
            print(help_string)
            sys.exit()
        elif opt in ("-i", "--input"):
            input_file = arg
            print(input_file)
        elif opt in ("-w", "--workers"):
            print(arg, type(arg))
            try:
                desired_workers = int(arg)
            except:
                print("Number of workers must be an integer")
            

    if input_file.endswith(".csv"):
        return input_file, desired_workers
    else:
        print("Error: A .csv file containing simulation parameters is required")
        print(help_string)
        sys.exit(2)



#Creates threads of run_thread method. Pool-size = threads - 1. Each thread result is mapped to a variable that is
#returned when all processes are finished
def grow_phenotype(individuals, num_cpus):

    """using multithreading"""    
    # p = Pool(num_cpus)
    # new_individuals = p.map(evo.generate_phenotype, individuals)

    """using tqdm (progressbar)"""
    print(f"(using {num_cpus} CPU cores)")
    new_individuals = process_map(
        evo.generate_phenotype,
        individuals,
        max_workers=num_cpus
    )

    return new_individuals

"""
PROGRAM

"""

# initialize the evolution 
evo_start_time = time.time()
evolution_parameters = list()
input_file, n_workers = process_arguments()
with open(input_file, newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    reader_iter = iter(reader)
    header = next(reader_iter)
    for row in reader_iter:
        evolution_parameters.append({
            # "MODEL_TYPE": TYPE["CA"],
            "MODEL_TYPE": TYPE[str(row[0])],
            # Size of array
            "DIMENSION": int(row[1]),
            #Number of individuals in the population
            "POPULATION_SIZE" : int(row[2]),
            #Number of generations to run. Each generation will run a number og simulations equal to POPULATION_SIZE
            "NUM_GENERATIONS": int(row[3]),
            #Simulation duration in seconds
            "SIMULATION_DURATION": int(row[4]),
            #Number of simulation iterations per second
            "TIME_STEP_RESOLUTION": int(row[5]),
            #Chance for mutation for each gene selection
            "MUTATION_P": float(row[6]),
            #Percentage of current population that will create offspring
            "PARENTS_P": float(row[7]),
            #Percentage of current population that will be included in next generation
            "RETAINED_ADULTS_P": float(row[8]),
            #Name of the file of experimental data used as reference for fitness function and raster plot
            # "REFERENCE_PHENOTYPE": "Small - 7-1-35.spk.txt"
            "REFERENCE_PHENOTYPE": row[9]
        })

    
# set desired numbers of cpu, if none is given it will use all available
if n_workers:
    if n_workers < os.cpu_count():
        num_cpus = n_workers
    else:
        num_cpus = os.cpu_count()
else:
    num_cpus = os.cpu_count()

for evo_i, params in enumerate(evolution_parameters):
    model_start_time = time.time()
    
    # print summary of the running simulation parameters
    print("\n-------------------------------------")
    print(f"Running simulation {evo_i+1}/{len(evolution_parameters)}:")
    iterator = iter(params)
    key = next(iterator)
    print(f"{key}: {params[key][0]} (genome size = {params[key][1]})")
    for key in iterator:
        print(f"{key}: {params[key]}")


    # Creates population object with POPULATION_SIZE. 
    # Creates the set of genes that apply to this specific population
    pop = Population.Population(
        params["POPULATION_SIZE"], 
        params["MODEL_TYPE"][1] # size of genome
        )

    # Creates Evolution object with parameters set 
    evo = Evolution.Evolution(params)

    # Inititate variables
    fitness_trend = []
    average_fitness_trend = []
    parameter_trend = []
    generation_summary = {}


    # Start the evolution. Runs loop for NUM_GENERATIONS
    
    for i in range(params["NUM_GENERATIONS"]):
        print(f"\nGeneration {i+1}/{params['NUM_GENERATIONS']}", end=" ")
        # print("Workers: ", end="")
        pop_with_phenotypes = grow_phenotype(pop.individuals, num_cpus)

        # Record data of pupulation
        fitness_trend.append([i.fitness for i in pop_with_phenotypes])
        average_fitness_trend.append(sum([i.fitness for i in pop_with_phenotypes])/params["POPULATION_SIZE"])
        parameter_trend.append(np.sum([i.genotype for i in pop_with_phenotypes],0)/params["POPULATION_SIZE"])
        
        # Updates best individual if better than current best
        sorted_pop = pop_with_phenotypes
        sorted_pop.sort(key=lambda x: x.fitness, reverse=True)

        # Save data of top 5 individuals
        if i % 5 == 0 or i+1 == params["NUM_GENERATIONS"]:
            top5_summary = {}
            top5 = sorted_pop[:5]
            for j in range(5):
                top5_summary[f"rank {j+1}"] = {
                    # "generation" : i,
                    # "rank" : j+1,
                    "genotype" : top5[j].genotype,
                    "phenotype" : top5[j].phenotype.tolist(),
                    "fitness" : top5[j].fitness,
                    }
            generation_summary[i+1] = top5_summary


        #   If there is no recorded best individual, choose the best one of this generation
        if not evo.best_individual_overall:
            evo.best_individual_overall = (i, sorted_pop[0])

        #   If the fitness of the best individual in this generation is better than the best recorded individual,
        #   let the new one take its place as the best.
        elif evo.best_individual_overall[1].fitness < sorted_pop[0].fitness:
            evo.best_individual_overall = (i, sorted_pop[0])

        # Reproduce
        if i < params["NUM_GENERATIONS"] - 1:
            parents = evo.select_parents(pop_with_phenotypes)
            new_gen = evo.reproduce(parents, pop_with_phenotypes)
            pop.individuals = new_gen
            print()
        else:
            pop.individuals = pop_with_phenotypes

    # Register the time it took to run the script
    model_total_time = time.time() - model_start_time

    # Save summary
    print("Saving summary to output folder...")
    summary = Summary.Summary(pop, params, evo)
    summary.raster_plot()
    summary.fitness_trend_plot((fitness_trend, average_fitness_trend))
    summary.parameter_trend_plot(parameter_trend)
    summary.average_distance_plot()
    summary.output_text(model_total_time)
    summary.save_model(evo.best_individual_overall[1].model)
    summary.save_stats(generation_summary)
    print(f"Model simulated in {model_total_time:.2f} seconds")

evo_total_time = round(time.time() - evo_start_time)
print(f"Evolution complete. Simulated in {evo_total_time // 60} minutes, {evo_total_time % 60} seconds")

