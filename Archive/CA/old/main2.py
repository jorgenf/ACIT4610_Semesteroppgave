from multiprocessing import Process, Queue
import matplotlib
matplotlib.use("TkAgg")
from pylab import *
from CA import fitness_functions, CA_model, data, population

def __run_proc(DNA, queue):
    result = CA_model.Neuron_model(DNA, duration= 10).run_simulation()
    correlation = fitness_functions.normalized_circular_cross_correlation(result, data.get_firing_rate("Small - 7-1-35.spk.txt"))
    print(correlation)
    DNA.set_fitness(correlation)
    queue.put(DNA)

def evolve_generation(DNAs):
    if __name__ == '__main__':
        queue = Queue()
        jobs = []
        for DNA in DNAs:
            p = Process(target=__run_proc,args=(DNA, queue))
            jobs.append(p)
            while 10 < len([proc.is_alive() for proc in jobs]):
                pass
            p.start()
            print("Started", p.name, p.pid, "...")
        while [i for i in jobs if i.is_alive()]:
            for j in jobs:
                if not j.is_alive():
                    jobs.remove(j)
        DNAs = []
        while not queue.empty():
            DNAs.append(queue.get())
    return DNAs

population = population.Population(10)
DNAs = population.get_individuals()
new_gen = evolve_generation(DNAs)
print(new_gen)
while not new_gen:
    pass
print(new_gen[0].get_fitness())
population.update_DNAs(new_gen)
dnas = population.get_individuals()
print("First")
for i in range(len(dnas)):
    print(dnas[i].p, dnas[i].reset_n, dnas[i].spont_p, dnas[i].neighbour_width, dnas[i].get_fitness())
population.mix_DNAs()
dnas = population.get_individuals()
print("Second")
for i in range(len(dnas)):
    print(dnas[i].p,dnas[i].reset_n, dnas[i].spont_p, dnas[i].neighbour_width, dnas[i].corr)
