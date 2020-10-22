from multiprocessing import *
import matplotlib
from CA import fitness_functions, CA_model, data, population, evolution
matplotlib.use("TkAgg")
import os

MODEL_TYPE = "CA"
POPULATION_SIZE = 10
NUM_GENERATIONS = 2
SIMULATION_DURATION = 1
TIME_STEP_RESOLUTION = 1
FITNESS_FUNCTION = "Normalized cross correlation"

def run_proc(individual):
    print(current_process().name, end="  ")
    phenotype = CA_model.Neuron_model(individual, duration= SIMULATION_DURATION, resolution = TIME_STEP_RESOLUTION).run_simulation()
    individual.set_phenotype(phenotype)
    fitness = fitness_functions.cross_correlation(phenotype, data.get_firing_rate("Small - 7-1-35.spk.txt"))
    individual.set_fitness(fitness)
    return individual

if __name__ == '__main__':

    def generate_phenotypes(individuals):
        p = Pool(os.cpu_count()-1)
        new_individuals = p.map(run_proc, individuals)
        return new_individuals


    pop = population.Population(POPULATION_SIZE)
    evo = evolution.Evolution(0.1, 0.5,0.05)
    print("Running simulation...")
    for i in range(NUM_GENERATIONS):
        print("\nGeneration:", i)
        print("Workers: ", end="")
        pop.update_individuals(generate_phenotypes(pop.get_individuals()))
        new_gen = evo.get_next_generation(pop.get_individuals())
        pop.update_individuals(new_gen)
    individuals = pop.get_individuals()
    print(len(individuals))
    for i in range(len(individuals)):
        print(individuals[i].genotype[0], individuals[i].genotype[1], individuals[i].genotype[2], individuals[i].genotype[3])

