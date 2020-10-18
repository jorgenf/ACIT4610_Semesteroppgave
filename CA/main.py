from multiprocessing import *
import matplotlib
matplotlib.use("TkAgg")
from pylab import *
from CA import fitness_functions, CA_model, data, population
import os

MODEL_TYPE = "CA"
POPULATION_SIZE = 100
NUM_GENERATIONS = 10
SIMULATION_DURATION = 10
TIME_STEP_RESOLUTION = 10
FITNESS_FUNCTION = "Normalized cross correlation"

def run_proc(DNA):
    print(current_process().name, end="  ")
    result = CA_model.Neuron_model(DNA, duration= SIMULATION_DURATION, resolution = TIME_STEP_RESOLUTION).run_simulation()
    DNA.set_spike_graph(result)
    fitness = fitness_functions.cross_correlation(result, data.get_firing_rate("Small - 7-1-35.spk.txt"))
    DNA.set_correlation(fitness)
    return DNA

if __name__ == '__main__':

    def evolve_generation(DNAs):
        p = Pool(os.cpu_count()-1)
        DNAs = p.map(run_proc, DNAs)
        return DNAs

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
        population.update_DNAs(evolve_generation(population.get_DNAs()))
        population.mix_DNAs()
    dnas = population.get_DNAs()
    print(len(dnas))
    for i in range(len(dnas)):
        print(dnas[i].p,dnas[i].reset_n, dnas[i].spont_p, dnas[i].neighbour_width)
