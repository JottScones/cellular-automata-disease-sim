import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
import random as r
from functools import reduce
import math

# setting up the values for the grid
R = 2  # Recovered
S = 1  # Susceptible
I = 0 # Infected

starting_vals = [I, S, R]

def init_grid_colors(N):
    return np.random.choice(starting_vals, N*N, p=[0.1, 0.8, 0.1]).reshape(N, N)

def random_grid(N, IPOP):
    # Returns a random grid with IPOP proportion of infected people
    return np.random.choice(starting_vals, N*N, p=[IPOP, 1 - IPOP, 0.0]).reshape(N, N)

def central_infection(N, IPOP):
    # Returns a grid with IPOP proportion of infected people in center
    cent_size = round(N * IPOP)
    central   = np.ones(cent_size)
    edge1     = np.zeros(math.floor((N - cent_size) / 2))
    edge2     = np.zeros(math.ceil((N - cent_size) / 2))
    filter    = np.concatenate((edge1, central, edge2))
    return 1 - np.ones((N, N)) * filter * filter.reshape((N, 1))

def get_cell(x, y, grid):
    # Get cell function that ensures coord are within grid
    N = grid.shape[0]
    if (y < 0 or y >= N or x < 0 or x >= N):
        return -1
    else:
        return grid[x][y]

def num_inf_neighbours(x, y, grid):
    # Helper function that counts the number of infected surrounding neighbours
    neighbours = np.array([
                            [-1, -1], [-1, 0], [-1, 1],
                            [0,  -1],          [0,  1],
                            [1,  -1], [1,  0], [1,  1]
                            ])
    neighbours_coord   = (neighbours + [x, y]).tolist()
    sum_infected       = lambda tot, c: tot + (get_cell(c[0], c[1], grid) == 0)
    num_inf_neighbours = reduce(sum_infected, neighbours_coord, 0)

    return num_inf_neighbours


def update(frameNum, img, grid, N, PI, PR, PRI):
    # Update function for drawing the cellular automata
    newGrid = grid.copy()

    for i in range(N):
        for j in range(N):
            if grid[i][j] == 0:
                # Use PR to decide if infected cell recovers
                newGrid[i][j] = (PR > r.random()) * 2
            elif grid[i][j] == 2:
                # Use PRI to decide if recovered cell is infected again
                inf_neighbors = num_inf_neighbours(i, j, grid)
                prob_infected = 1 - (1 - PRI) ** inf_neighbors
                newGrid[i][j] = (prob_infected < r.random()) * 2
            else:
                # Use PI to decide if susceptible cell is infected
                inf_neighbors = num_inf_neighbours(i, j, grid)
                prob_infected = 1 - (1 - PI) ** inf_neighbors
                newGrid[i][j] = 0 + (prob_infected < r.random())

    # Update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

def update_pop(frameNum, ax, grid, R, S, I):
    # Update function for drawing pop. of Recovered, Susceptible & Infected
    curr_r = np.sum(grid == 2)
    curr_s = np.sum(grid == 1)
    curr_i = np.sum(grid == 0)

    R.append(curr_r)
    S.append(curr_s)
    I.append(curr_i)

    ax.clear()
    ax.plot(R, label="Recovered")
    ax.plot(S, label="Susceptible")
    ax.plot(I, label="Infected")
    ax.legend()

def draw_grid():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED   = (255, 0, 0)

# main() function
def main():
    # Create a command line parse for arguments
    parser = argparse.ArgumentParser(description="Runs a disease simulator")

    # Add arguments
    parser.add_argument('--infect-prob', dest='PI', required=True)
    parser.add_argument('--recover-prob', dest='PR', required=True)
    parser.add_argument('--recov-infect-prob', dest='PRI', required=False)
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--infect-pop', dest='IPOP', required=False)
    parser.add_argument('--grid-type', dest='GT', required=False)

    args = parser.parse_args()

    PI  = float(args.PI) # Prob of infectstion
    PR  = float(args.PR) # Prob of recovery

    # Set prob of reinfection (default: 0)
    PRI = 0
    if args.PRI and float(args.PRI) <= 1 and float(args.PRI) >= 0:
        PRI = float(args.PRI)

    # Set grid size (default: 50)
    N = 50
    if args.N and int(args.N) > 8:
        N = int(args.N)

    IPOP = 0.1
    if args.IPOP and float(args.IPOP) <= 1 and float(args.IPOP) >= 0:
        IPOP = float(args.IPOP)

    # Set grid type (default: random)
    GT    = random_grid(N, IPOP)
    GNAME = 'Random'
    if args.GT and args.GT == 'central':
        GT = central_infection(N, IPOP)
        GNAME = 'Central'

    # set animation update interval
    updateInterval = 50

    fig, axs = plt.subplots(1, 2, figsize=(15,4))
    fig.canvas.set_window_title(GNAME+ ' Infection Sim: Pop='+ str(N * N) + ' IPOP=' + str(IPOP) + ' PI=' + str(PI) + ' PR=' + str(PR) + ' PRI=' + str(PRI))

    ax1 = axs[0]
    ax1.axis("off")
    ax2 = axs[1]
    ax2.set_aspect('auto')

    colors = ['red', 'yellowgreen', 'lightblue']
    cmap = mpl.colors.ListedColormap(colors)

    # Workaround for ensuring color is assigned to every value
    grid = init_grid_colors(N)
    img  = ax1.imshow(grid, interpolation='none', cmap=cmap)
    grid = GT
    img.set_data(grid)

    # Population Array initialisation for pop graph animation
    R = []
    S = []
    I = []

    ani1 = animation.FuncAnimation(fig, update, fargs=(img, grid, N, PI, PR, PRI), frames=10, interval=updateInterval, blit=True)
    ani2 = animation.FuncAnimation(fig, update_pop, fargs=(ax2, grid, R, S, I), frames=10, interval=updateInterval)

    plt.show()

# call main
if __name__ == '__main__':
    main()
