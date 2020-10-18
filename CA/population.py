import matplotlib
matplotlib.use("TkAgg")
from pylab import *


SPLIT = 2
MUTATION = 0.1

class Population:
    def __init__(self, num_DNA=100):
        self.num_DNA = num_DNA
        self.DNAs = self.__initiate_DNAs(self.num_DNA)

    def __initiate_DNAs(self, num_DNA):
        DNAs = []
        for n in range(num_DNA):
            while True:
                p = randint(3, 11) / 10
                neighbor_width = randint(1, 11)
                spont_p = randint(1, 20) / 100000
                reset_n = randint(1, 21)
                if DNAs:
                    exist = False
                    for dna in DNAs:
                        if p == dna.p and neighbor_width == dna.neighbour_width and spont_p == dna.spont_p and reset_n == dna.reset_n:
                            exist = True
                    if not exist:
                        DNAs.append(DNA(p, neighbor_width, spont_p, reset_n))
                        break
                else:
                    DNAs.append(DNA(p, neighbor_width, spont_p, reset_n))
                    break
        return DNAs

    def get_DNAs(self):
        return self.DNAs

    def update_DNAs(self, DNAs):
        self.DNAs = DNAs

    def mix_DNAs(self):
        self.DNAs.sort(key = lambda x : x.corr, reverse=True)
        best_DNAs = self.DNAs[:len(self.DNAs)//SPLIT]
        mixed_DNAs = []
        for dna in range(len(self.DNAs)):
            mixed_DNAs.append(DNA(randint(3, 11) / 10 if random() < MUTATION else best_DNAs[randint(len(best_DNAs))].p, randint(1, 11) if random() < MUTATION else best_DNAs[randint(len(best_DNAs))].neighbour_width, randint(1, 20) / 100000 if random() < MUTATION else best_DNAs[randint(len(best_DNAs))].spont_p, randint(1, 21) if random() < MUTATION else best_DNAs[randint(len(best_DNAs))].reset_n))
        self.DNAs = mixed_DNAs


class DNA:
    def __init__(self, p, neighbour_width, spont_p, reset_n):
        self.p = p
        self.neighbour_width = neighbour_width
        self.spont_p = spont_p
        self.reset_n = reset_n

    def set_correlation(self, corr):
        self.corr = corr

    def get_correlation(self):
        return self.corr

    def set_spike_graph(self, spike_graph):
        self.spike_graph = spike_graph

    def get_spike_graph(self):
        return self.spike_graph
