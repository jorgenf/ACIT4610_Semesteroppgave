import csv
import numpy as np
import matplotlib.pyplot as plt
import os
import Data

class Summary:
    def __init__(self, population, evolution_parameters, evo):
        self.population = population
        self.evolution_parameters = evolution_parameters
        self.population.individuals.sort(key=lambda x: x.fitness, reverse=True)
        self.median_individual = self.population.individuals[int(round(len(self.population.individuals)/2))]
        self.best_individual = self.population.individuals[0]
        self.best_individual_overall = evo.best_individual_overall
        self.top_five = self.population.individuals[0:5] if len(self.population.individuals) >= 5 else False
        self.reference_spikes = Data.get_spikes_file(self.evolution_parameters["REFERENCE_PHENOTYPE"])
        self.simulation_spikes = Data.get_spikes_pheno(self.best_individual.phenotype, self.evolution_parameters["SIMULATION_DURATION"])
        self.dir_path = "Output/"+ self.evolution_parameters["MODEL_TYPE"][0] + "_dim" + str(self.evolution_parameters["DIMENSION"]) + "_pop" + str(self.evolution_parameters["POPULATION_SIZE"]) + "_gen" + str(self.evolution_parameters["NUM_GENERATIONS"]) + "_dur" + str(self.evolution_parameters["SIMULATION_DURATION"]) + "_res" + str(self.evolution_parameters["TIME_STEP_RESOLUTION"]) + "_mut" + str(self.evolution_parameters["MUTATION_P"]) + "_par" + str(self.evolution_parameters["PARENTS_P"]) + "_ret" + str(self.evolution_parameters["RETAINED_ADULTS_P"]) + "_version"
        if os.path.exists(self.dir_path + str(0)):
            n = 1
            while os.path.exists(self.dir_path + str(n)):
                n += 1
            self.dir_path += str(n)
            os.makedirs(self.dir_path)
        else:
            self.dir_path += str(0)
            os.makedirs(self.dir_path)

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

        fig.savefig(self.dir_path + "/Best_individual.png")

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
        par.savefig(self.dir_path + "/Parameter_trend.png")
    
    def fitness_trend_plot(self, fitness_data):
        avg_fit, ax_avg_fit = plt.subplots()
        ax_avg_fit.plot(fitness_data[0], linestyle="",marker=".", color="red")
        ax_avg_fit.plot(fitness_data[1], label="Average fitness", color="blue")
        ax_avg_fit.legend(loc="upper left")
        ax_avg_fit.set_title("Fitness trend")
        ax_avg_fit.set_xlabel("Generation")
        ax_avg_fit.set_ylabel("Fitness score")
        ax_avg_fit.set_ylim(ymin=0, ymax=1)
        avg_fit.savefig(self.dir_path + "/Fitness_trend.png")

    def average_distance_plot(self):
        simulation_s = sorted(self.simulation_spikes)
        reference_s = sorted(self.reference_spikes[:len(self.simulation_spikes)])
        simulation = self.simulation_spikes
        reference = self.reference_spikes[:len(simulation)]
        fig, ax = plt.subplots(2, sharex="all")
        ax[0].set_xlabel("Sorted time [s]")
        ax[0].set_ylabel("Spikes per second")
        ax[0].plot(simulation_s, 'b', label="Simulation")
        ax[0].plot(reference_s, 'black', label="Reference")
        ax[0].plot([abs(sim - ref) for ref, sim in zip(simulation_s, reference_s)], label="Difference")
        ax[0].legend()
        ax[0].fill_between(range(len(simulation_s)), simulation_s, reference_s, color='red', alpha=0.2,
                           where=[_y2 < _y1 for _y2, _y1 in zip(simulation_s, reference_s)])
        ax[0].fill_between(range(len(simulation_s)), simulation_s, reference_s, color='green', alpha=0.2,
                           where=[_y2 > _y1 for _y2, _y1 in zip(simulation_s, reference_s)])
        for i in range(0, len(simulation_s), int(len(simulation_s) / 10)):
            ax[0].text(i, min(simulation_s[i], reference_s[i]) + 30, simulation_s[i] - reference_s[i])

        ax[1].set_xlabel("Time [s]")
        ax[1].set_ylabel("Spikes per second")
        ax[1].plot(simulation, 'b', label="Simulation")
        ax[1].plot(reference, 'black', label="Reference")
        ax[1].legend()
        ax[1].fill_between(range(len(simulation)), simulation, reference, color='red', alpha=0.2,
                           where=[_y2 < _y1 for _y2, _y1 in zip(simulation, reference)])
        ax[1].fill_between(range(len(simulation)), simulation, reference, color='green', alpha=0.2,
                           where=[_y2 > _y1 for _y2, _y1 in zip(simulation, reference)])
        fig.savefig(self.dir_path + "/Average_distance.png")


    def output_text(self, simulation_time):
        if self.top_five:
            top_five_string = "| INDIVIDUAL 2 | " + "Parameters: " + str(self.top_five[1].genotype) + " Fitness score: " + str(self.top_five[1].fitness) + "\n" + "| INDIVIDUAL 3 | " + "Parameters: " + str(self.top_five[2].genotype) + " Fitness score: " + str(self.top_five[2].fitness) + "\n" + "| INDIVIDUAL 4 | " + "Parameters: " + str(self.top_five[3].genotype) + " Fitness score: " + str(self.top_five[3].fitness) + "\n" + "| INDIVIDUAL 5 | " + "Parameters: " + str(self.top_five[4].genotype) + " Fitness score: " + str(self.top_five[4].fitness) + "\n" + "TOP 5 AVERAGE: " + str((sum([self.top_five[i].fitness for i in range(1,5)]) + self.best_individual.fitness) / 5)
        else:
            top_five_string = ""
        text_file = open(self.dir_path + "/Info.txt", "wt")
        n = text_file.write("EVOLUTION PARAMETERS: " + str(self.evolution_parameters) + " Simulation time [min]: " + str(simulation_time/60) + "\n" + "*LAST GENERATION*" + "\n| INDIVIDUAL 1 | " + "Parameters: " + str(self.best_individual.genotype) + " Fitness score: " + str(self.best_individual.fitness) + "\n" + top_five_string + "\n" + "| MEDIAN INDIVIDUAL |" + " Fitness score: " + str(self.median_individual.fitness) + "\n\nBEST OVERALL\n" + "| TOP INDIVIDUAL | " + "Generation: " + str(self.best_individual_overall[0]) + " Parameters: "+ str(self.best_individual_overall[1].genotype) + " Fitness score: " + str(self.best_individual_overall[1].fitness))
        text_file.close()


    def write_csv(self, fitness_data):
        with open(self.dir_path + "/fitness.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter='\t')
            writer.writerow(["generation", "avg_fitness"])
            for i, score in enumerate(fitness_data):
                writer.writerow([str(i), str(score)])

