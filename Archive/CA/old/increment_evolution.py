import matplotlib
matplotlib.use("TkAgg")
from pylab import *



class Evolution:
    def __init__(self, comparing_file="Data/Small - 7-1-35.spk.txt",  num_DNA=16):
        self.comparing_file = comparing_file
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

