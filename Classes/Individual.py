import numpy as np

#   Genetic Encoding for the model
genotype = []
#   Whatever the model outputs
phenotype = np.array()
#   Result of fitness function
fitness = 0


class Individual:
    """
    Individuals consist of a genotype and a phenotype.
    The genotype is the genetic encoding of the individual.
    The phenotype is the part of the individual that is tested in the environment.
    The fitness is a score or a result of a fitness function.
    """
    def __init__(self, g_type=genotype, p_type=phenotype, f_ness=fitness):
        self.genotype = g_type
        self.phenotype = p_type
        self.fitness = f_ness
