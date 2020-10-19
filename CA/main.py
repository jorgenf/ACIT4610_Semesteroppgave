from multiprocessing import *
import matplotlib

from ACIT4610_Semesteroppgave.CA import fitness_functions, CA_model, data, population

matplotlib.use("TkAgg")
from pylab import *
#from CA import fitness_functions, CA_model, data, population
import os

MODEL_TYPE = "CA"
POPULATION_SIZE = 100
NUM_GENERATIONS = 10
SIMULATION_DURATION = 10
TIME_STEP_RESOLUTION = 10
FITNESS_FUNCTION = "Normalized cross correlation"

def run_proc(genotype):
    print(current_process().name, end="  ")
    phenotype = CA_model.Neuron_model(genotype, duration= SIMULATION_DURATION, resolution = TIME_STEP_RESOLUTION).run_simulation()
    genotype.set_phenotype(phenotype)
    fitness = fitness_functions.cross_correlation(phenotype, data.get_firing_rate("Small - 7-1-35.spk.txt"))
    genotype.set_fitness(fitness)
    return genotype

if __name__ == '__main__':

    def generate_phenotypes(genotypes):
        p = Pool(os.cpu_count()-1)
        genotypes = p.map(run_proc, genotypes)
        return genotypes

    print("Choose model type:\n1. CA\n2. Network")
    MODEL_TYPE = int(input("Choice: "))
    POPULATION_SIZE = int(input("Choose population size: "))
    NUM_GENERATIONS = int(input("Choose number of generations: "))
    SIMULATION_DURATION = int(input("Choose simulation duration in seconds: "))
    TIME_STEP_RESOLUTION = int(input("Choose simulation iterations per second: "))
    print("Choose fitness-function:\n1. Cross-correlation\n2. Normalized cross-correlation\n3. Circular cross-correlation\n4. Normalized circular cross-correlation\n5. Average distance")
    FITNESS_FUNCTION = int(input("Choice: "))


    population = population.Population(POPULATION_SIZE)
    print("Running simulation...")
    for i in range(NUM_GENERATIONS):
        print("\nGeneration:", i)
        print("Workers: ", end="")
        population.update_genotypes(generate_phenotypes(population.get_genotypes()))
        parents = population.select_parents()
        population.update_genotypes(population.reproduce(parents))
    dnas = population.get_genotypes()
    print(len(dnas))
    for i in range(len(dnas)):
        print(dnas[i].p,dnas[i].reset_n, dnas[i].spont_p, dnas[i].neighbour_width)
