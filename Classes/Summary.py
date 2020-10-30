import numpy as np
import matplotlib.pyplot as plt

import Data

class Summary:
    def __init__(self, population, evolution_parameters):
        self.population = population
        self.evolution_parameters = evolution_parameters

        self.population.individuals.sort(key=lambda x: x.fitness, reverse=True)
        self.best_individual = self.population.individuals[0]
        print(self.best_individual)
    
    def raster_plot(self):
        """
        Takes two phenotypes as input and plot them side-by-side as raster plot and histogram

        Assumes phenotype is a list of lists or 2D numpy array similar to:
        [[.00396, 56],
        [0.05284, 16],
        [0.05800, 15],
        ...,
        [A, B]]
        Where A is a timestamp and B is electrode ID (must be a integer between 0-63)

        To create histogram it is necessary to specify bin-size. For spikes per second "bin_size" = simulation length [seconds]
        """

        self.phenotype_reference = Data.read_recording(
            self.evolution_parameters["REFERENCE_PHENOTYPE"], 
            recording_len = self.evolution_parameters["SIMULATION_DURATION"],
            recording_start= 0 # where to start reading experimental data [s]
            )

        self.bin_size = self.evolution_parameters["SIMULATION_DURATION"]
        
        # check if input is correct format    
        self.best_individual.phenotype = np.array(
            [(row[0], row[1]) for row in self.best_individual.phenotype], 
            dtype=[("t", "float64"), ("electrode", "int64")])
        self.phenotype_reference = np.array(
            [(row[0], row[1]) for row in self.phenotype_reference], 
            dtype=[("t", "float64"), ("electrode", "int64")])

        # sort spikes by electrode
        self.A_spikes_per_array = [ [] for _ in range(64)]
        for row in self.best_individual.phenotype:
            self.A_spikes_per_array[row[1]].append(row[0])

        self.B_spikes_per_array = [ [] for _ in range(64)]
        for row in self.phenotype_reference:
            self.B_spikes_per_array[row[1]].append(row[0])

        # initiate plot
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, sharex="all", sharey="row")

        # make raster plots
        ax1.eventplot(
            self.A_spikes_per_array,
            linewidths=0.5
            )
        ax1.set_xlabel("Seconds")
        ax1.set_ylabel("Electrode ID")
        ax1.set_title("Best model")
        
        ax2.eventplot(
            self.B_spikes_per_array,
            linewidths=0.5,
            color = "black"
            )
        ax2.set_xlabel("Seconds")
        ax2.set_title("Neural culture")

        # make histograms
        ax3.hist(self.best_individual.phenotype["t"], bins=self.bin_size)
        ax3.set_xlabel("Seconds")
        ax3.set_ylabel("Spikes per second")

        ax4.hist(self.phenotype_reference["t"], bins=self.bin_size, color="black")
        ax4.set_xlabel("Seconds")
        
        # return plt
        plt.show()

        # self.raster_plot_fig = fig

    def parameter_trend_plot(self, parameter_data):
        # Plot parameter trend
        par, ax_par = plt.subplots()
        for param, label in zip(list(map(list, zip(*parameter_data))), self.evolution_parameters["MODEL_TYPE"][2]):
            ax_par.plot(param, label=label)
        #ax_par.plot(parameter_data, label="Parameter")
        ax_par.legend(loc="upper left")
        ax_par.set_title("Parameter trend")
        ax_par.set_xlabel("Generation")
        ax_par.set_ylabel("Normalized genome value")
        par.savefig("Output/Parameter_trend.png")
    
    def fitness_trend_plot(self, fitness_data):
        avg_fit, ax_avg_fit = plt.subplots()
        ax_avg_fit.plot(fitness_data[1], label="Average fitness")
        ax_avg_fit.plot(fitness_data[0], linestyle="",marker=".", color="red")
        ax_avg_fit.legend(loc="upper left")
        ax_avg_fit.set_title("Fitness trend")
        ax_avg_fit.set_xlabel("Generation")
        ax_avg_fit.set_ylabel("Fitness score")
        # avg_fit.savefig("Output/Fitness_trend_" + str(MODEL_TYPE) + "_" + str(POPULATION_SIZE) + "_" + str(NUM_GENERATIONS) + "_" + str(SIMULATION_DURATION) + "_" + str(TIME_STEP_RESOLUTION) + "_" + str(MUTATION_P) + "_" + str(PARENTS_P) + "_" + str(RETAINED_ADULTS_P) + ".png")
        avg_fit.savefig("Output/Fitness_trend")
        