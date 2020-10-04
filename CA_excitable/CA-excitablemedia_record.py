from pylab import *

# params for CA model
width = 32
height = width # want a square
initProb = 0.01
maxState = 5
dt = .01 # t = seconds

# params for simulation recording
simulation_length = 10 # seconds
start_t = 50 # ignore first iterations
dt = dt # set here or as CA param?

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

ca_exite_data = []
mea_exite_data = []
mea_data = zeros([mea_height, mea_width])
simulation_output = []

# def initialize():
# global time, config, nextConfig

time = 0

config = zeros([height, width])
for x in range(width):
    for y in range(height):
        if random() < initProb:
            state = maxState
        else:
            state = 0
        config[y, x] = state

nextConfig = zeros([height, width])



# def update():
#     global time, config, nextConfig¨
while time < ((simulation_length // dt) + start_t):
    time += 1

    for x in range(width):
        for y in range(height):
            state = config[y, x]
            if state == 0:
                num = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if config[(y+dy)%height, (x+dx)%width] == maxState:
                            num += 1
                if random() * 3 < num:
                    state = maxState
                else:
                    state = 0
            else:
                state -= 1
            nextConfig[y, x] = state
            if x%8 == 0 and y%8==0:
                coords = (y//8, x//8)
                mea_data[coords] = state
                if state == maxState:
                    if coords not in inactive_cells: # dont want to record the inactive electrodes
                        if time > start_t: # dont want to record first iterations
                            simulation_output.append(f"{time*dt} {1*x//8 + 8*y//8}")


    config, nextConfig = nextConfig, config
    if time%(1//dt) == 0:
        print(time)

with open("CA_excitable\simulation_data.txt", "w") as f:
    for line in simulation_output:
        f.write(line + "\n")