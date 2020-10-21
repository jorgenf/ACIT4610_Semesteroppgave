from pylab import *

# params for CA model
width = 10*10 # multiples of ten
height = width # want a square
initProb = 0.001
maxState = 10
dt = .1 # t = seconds

# params for simulation recording
simulation_length = 120 # seconds
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

# which cells are regarded part of MEA
node_cells = []
for x in range(1, mea_width+1):
    for y in range(1, mea_height+1):
        node_cells.append((
            x * (width // (mea_width + 2)),
            y * (height // (mea_height + 2))
        ))

x_division = width // (mea_width + 2) 
y_division = height // (mea_height + 2)

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
            # if x%x_division == 0 and y%y_division == 0:
            if (y, x) in node_cells:
                coords = (y//y_division-1, x//x_division-1)
                # print(coords)
                mea_data[coords] = state
                if state == maxState:
                    if coords not in inactive_cells: # dont want to record the inactive electrodes
                        if time > start_t: # dont want to record first iterations
                            simulation_output.append(f"{(time-start_t+1)*dt} {1*coords[1] + 8*coords[0]}")


    config, nextConfig = nextConfig, config
    if time%(1//dt) == 0:
        print(f"Recorded seconds: {(time - start_t + 1) * dt}")

with open("CA_excitable\simulation_data.txt", "w") as f:
    for line in simulation_output:
        f.write(line + "\n")