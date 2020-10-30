import numpy as np
import matplotlib.pyplot as plt

import Data

class Summary:
    def __init__(self, population, evolution_parameters, fitness_trend):
        self.population = population
        self.evolution_parameters = evolution_parameters
        self.fitness_trend = fitness_trend

        self.population.individuals.sort(key=lambda x: x.fitness, reverse=True)
        self.best_individual = self.population.individuals[0]
        print(self.best_individual)
    
    def raster_plot(self):
        """
        Takes two phenotypes as input and plot them side-by-side as raster plot and histogram

        Assumes "phenotype_X" is a list of lists or 2D numpy array similar to:
        [[.00396, 56],
        [0.05284, 16],
        [0.05800, 15],
        ...,
        [A, B]]
        Where A is a timestamp and B is electrode ID (must be a integer between 0-63)

        To create histogram it is necessary to specify bin-size. For spikes per second "bin_size" = simulation length [seconds]
        """


        # self.phenotype_X = Data.read_recording(
        #     self.best_individual.phenotype,
        #     recording_len = self.evolution_parameters["SIMULATION_DURATION"],
        #     recording_start= 0 # where to start reading experimental data [s]
        #     )
        
        self.phenotype_reference = Data.read_recording(
            self.evolution_parameters["REFERENCE_PHENOTYPE"], 
            recording_len = self.evolution_parameters["SIMULATION_DURATION"],
            recording_start= 0 # where to start reading experimental data [s]
            )

        self.bin_size = self.evolution_parameters["SIMULATION_DURATION"]
        
        # raster_plot = Data.raster_plot(
        #     best_individual.phenotype, 
        #     Data.read_recording(
        #         REFERENCE_PHENOTYPE, 
        #         recording_len=SIMULATION_DURATION,
        #         recording_start=0 # where to start reading experimental data [s]
        #         ), 
        #     SIMULATION_DURATION
        # )

        
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
        