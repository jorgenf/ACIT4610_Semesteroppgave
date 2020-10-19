import numpy as np
import matplotlib.pyplot as plt

class CA_excitablemedia:
    def __init__(self, grid_size, initial_probability, max_state, dt):

        # params for CA model
        self.width = 10 * grid_size # multiples of ten
        self.height = self.width # want a square
        self.initial_probability = initial_probability
        self.max_state = max_state
        self.dt = dt # t = seconds

        print(grid_size, initial_probability, max_state, dt)

        # params for simulation recording
        self.simulation_length = 5 # seconds
        self.start_t = 10 # ignore first iterations
        self.dt = self.dt # set here or as CA param?

        # params for MEA
        self.mea_width = 8
        self.mea_height = self.mea_width
        self.inactive_cells = ( # 59 electrodes in experiment. corners inactive + a ground node
            (0,0),
            (1, 0), # ground node
            (self.mea_width-1, 0),
            (self.mea_width-1, self.mea_height-1),
            (0, self.mea_height-1)
            )

        # start simulation
        self.run()


    def run(self):        
        # set initial conditions
        self.initialize()

        # update model N times (given by by simulation_length and dt)
        while self.time < ((self.simulation_length // self.dt) + self.start_t):
            self.time += 1
            self.update()
            
        # export simulation result
        self.phenotype = self.simulation_output
        print(self.phenotype[:10])


    def initialize(self):
        # which cells are regarded part of MEA
        self.node_cells = []
        for x in range(1, self.mea_width+1):
            for y in range(1, self.mea_height+1):
                self.node_cells.append((
                    x * (self.width // (self.mea_width + 2)),
                    y * (self.height // (self.mea_height + 2))
                ))

        self.x_division = self.width // (self.mea_width + 2) 
        self.y_division = self.height // (self.mea_height + 2)

        # simulation data 
        # self.ca_exite_data = []
        # self.mea_exite_data = []
        self.mea_data = np.zeros([self.mea_height, self.mea_width])
        self.simulation_output = []

        # program variables
        self.time = 0

        self.config = np.zeros([self.height, self.width])
        for x in range(self.width):
            for y in range(self.height):
                if np.random.random_sample() < self.initial_probability:
                    self.state = self.max_state
                else:
                    self.state = 0
                self.config[y, x] = self.state

        self.nextConfig = np.zeros([self.height, self.width])

    
    def update(self):
        for x in range(self.width):
            for y in range(self.height):
                self.state = self.config[y, x]
                if self.state == 0:
                    self.num = 0
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            if self.config[(y+dy)%self.height, (x+dx)%self.width] == self.max_state:
                                self.num += 1
                    if np.random.random_sample() * 3 < self.num:
                        self.state = self.max_state
                    else:
                        self.state = 0
                else:
                    self.state -= 1
                self.nextConfig[y, x] = self.state
                # if x%self.x_division == 0 and y%self.y_division == 0:
                if (y, x) in self.node_cells:
                    self.coords = (y//self.y_division-1, x//self.x_division-1)
                    self.mea_data[self.coords] = self.state
                    if self.state == self.max_state:
                        if self.coords not in self.inactive_cells: # dont want to record the inactive electrodes
                            if self.time > self.start_t: # dont want to record first iterations
                                self.simulation_output.append((
                                    (self.time - self.start_t + 1) * self.dt, # spike time
                                    1 * self.coords[1] + 8 * self.coords[0] # spike on electrode id
                                    ))


        self.config, self.nextConfig = self.nextConfig, self.config
        if self.time%(1//self.dt) == 0:
            print(f"Recorded seconds: {(self.time - self.start_t + 1) * self.dt:.1f}")
    

if __name__ == "__main__":
    CA_excitablemedia(*[10, 0.001, 10, 0.1])
