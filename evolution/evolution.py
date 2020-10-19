import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from helpers import read_recording

from CA_excitablemedia import development


def initialize_child_genotypes():
    gtypes = list()
    for _ in range(generation_size):
        gtypes.append(( # genotype vector must be customized to model
            np.random.randint(1, 10), # grid_size
            round(np.random.rand(), 3), # initial_probability
            np.random.randint(1, 15), # max_state
            round(1 / np.random.randint(10, 20), 2) # dt
        ))
    return gtypes

def generate_phenotypes_from_genotypes(gtypes):
    ptypes = list()
    for genotype in gtypes:
        print(genotype)
        ptypes.append(development(*genotype, simulation_length))
    return ptypes


def test_fitness_of_phenotypes(ptypes):
    neuron_spikes, _ = read_recording(
        neural_data_filepath, 
        recording_start=60*1, # starting point in seconds
        recording_len=simulation_length # simlation length in seconds, set to match simulation
        )
    
    # bin the spikes in 1 second intervals
    neuron_sps = pd.cut(neuron_spikes, bins=simulation_length, precision=0)
    x = neuron_sps.value_counts().astype(np.float)

    fitness_scores = list()
    # print(ptypes)
    for ptype in ptypes:
        if ptype.size == 0: # dead if no items in array
            fitness_scores.append(0)
        else:
            sim_sps = pd.cut(ptype[:,0], bins=simulation_length, precision=0)
            y = sim_sps.value_counts().astype(np.float)

            corr = (plt.xcorr(x, y, usevlines=True, normed=True, maxlags=1, lw=2))
            fitness_scores.append(np.amax(corr[1]))
            # print("Best fit {} at {} lag" .format(
            #     np.amax(corr[1]),
            #     corr[0][np.where(corr[1] == np.amax(corr[1]))[0]][0]
            # ))
    
    # return phenotypes sorted by fitness score
    return sorted(zip(fitness_scores, ptypes), key=lambda x: x[0], reverse=True)




def adult_selection(scored_ptypes):
    pass


def parent_selection(ptypes):
    pass


def reproduction(ptypes):
    pass

# PROGRAM #

# parameters for evolution
n_generations = 1 # number of generations to run
generation_size = 10 # number of genotypes entered into each generation
simulation_length = 5 # length of the simulated output in seconds
neural_data_filepath = r"Data\Dense - 2-1-20.spk.txt" # experimental data used for comparison in fitness function

# evolutionary algorithm
generation = 0
genotypes = initialize_child_genotypes() # create some random initial genotypes
    
while generation < n_generations:

    # development
    young_phenotypes = generate_phenotypes_from_genotypes(genotypes) # run model with all genotypes
    young_phenotypes_scored = test_fitness_of_phenotypes(young_phenotypes) # score simulation result using fitness function
    
    # pruning
    adult_phenotypes = adult_selection(young_phenotypes_scored) # remove low scoring phenotypes
    parent_phenotypes = parent_selection(adult_phenotypes) # ??

    # reproduction
    new_genotypes = reproduction(parent_phenotypes) # ??

    generation += 1


alive = 0
for phen in young_phenotypes:
    if len(phen) > 0:
        alive += 1
print(f"Rate: {alive/generation_size}")