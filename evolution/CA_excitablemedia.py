import numpy as np
import matplotlib.pyplot as plt

def development(grid_size, initial_probability, max_state, dt, simulation_length):

    # params for CA model
    width = 10 * grid_size # multiples of ten
    height = width # want a square

    # params for simulation recording
    # simulation_length = 5 # seconds
    start_t = 10 # ignore first iterations

    # params for MEA
    mea_width = 8
    mea_height = mea_width
    inactive_cells = ( # 59 electrodes in experiment. corners inactive + a ground node
        (0,0),
        (1, 0), # ground node
        (mea_width-1, 0),
        (mea_width-1, mea_height-1),
        (0, mea_height-1)
        )

    # set initial conditions
    node_cells = []
    for x in range(1, mea_width+1):
        for y in range(1, mea_height+1):
            node_cells.append((
                x * (width // (mea_width + 2)),
                y * (height // (mea_height + 2))
            ))

    x_division = width // (mea_width + 2) 
    y_division = height // (mea_height + 2)

    # simulation data 
    mea_data = np.zeros([mea_height, mea_width])
    simulation_output = []

    # program variables
    time = 0

    config = np.zeros([height, width])
    for x in range(width):
        for y in range(height):
            if np.random.random_sample() < initial_probability:
                state = max_state
            else:
                state = 0
            config[y, x] = state

    nextConfig = np.zeros([height, width])

    # update model N times (given by by simulation_length and dt)
    while time < ((simulation_length // dt) + start_t):
        time += 1
        for x in range(width):
            for y in range(height):
                state = config[y, x]
                if state == 0:
                    num = 0
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            if config[(y+dy)%height, (x+dx)%width] == max_state:
                                num += 1
                    if np.random.random_sample() * 3 < num:
                        state = max_state
                    else:
                        state = 0
                else:
                    state -= 1
                nextConfig[y, x] = state
                # if x%x_division == 0 and y%y_division == 0:
                if (y, x) in node_cells:
                    coords = (y//y_division-1, x//x_division-1)
                    mea_data[coords] = state
                    if state == max_state:
                        if coords not in inactive_cells: # dont want to record the inactive electrodes
                            if time > start_t: # dont want to record first iterations
                                simulation_output.append((
                                    (time - start_t + 1) * dt, # spike time
                                    1 * coords[1] + 8 * coords[0] # spike on electrode id
                                    ))


        config, nextConfig = nextConfig, config
        # if time%(1//dt) == 0:
        #     print(f"Recorded seconds: {(time - start_t + 1) * dt:.1f}")
        
        time += 1

    # export simulation result
    return np.array(simulation_output)

if __name__ == "__main__":
    development(*[10, 0.001, 10, 0.1], 5)
