import random
import math
import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
from uuid import uuid4
from copy import copy
from models import Districting, Precinct

# Picks a random integer between 0 and n-1
pick_rand_idx = lambda n: int(math.floor(random.random()*n))

def main(step_length, trials, filepath):
    """
    Read in a user-defined districting and run the simulation

    Args:
        step_length (str): number of `flips` to do for the grid
        trials (int): number of separate simulations to run for this grid
        filepath (str): path to the json file specifying the districting
    """
    with open(filepath) as f:
        data = json.load(f)

    rows = len(data)
    cols = len(data[0])
    grid = np.empty(shape=(rows,cols), dtype=Precinct)
    row,col = (0,0)
    for d in data:
        if len(d) != cols:
            print 'ERROR: Provided json file has an invalid dimenstion'
            return

        for p in d:
            grid[row,col] = Precinct(p.get('party'), p.get('district_id'))
            col += 1
        row += 1
        col = 0

    dist = Districting(grid)
    if not dist.is_valid():
        print 'ERROR: Proposed districting is not valid'
        return

    original_eg = dist.get_efficiency_gap()

    fd = open('%s-results' % (str(uuid4())), 'w')
    fd.write("EG = %f\n\n%s\n----------------\n\n" % (original_eg, str(dist)))
    egs = []
    for t in range(trials):
        result, eg = simulate(step_length, dist)
        egs.append(eg)
        fd.write(str(dist) + '\n\n')
    fd.close()
    plt.title('Original EG = %f' % (original_eg,))
    plt.hist(egs)
    plt.show()


def simulate(length, dist):
    """
    Run a random walk for a given districting and determine the differing party counts

    Args:
        length (int): number of steps to take in the walk
        dist (numpy.ndarray): original districting before the simulation

    Returns:
        Districting: the resulting districting of the simulation
        float: the efficiency gap value for the resulting districting
    """

    # get party voting counts before the simulatinos
    for i in range(length):

        # pick a random cell in the grid
        row, col = pick_rand_idx(dist.rows), pick_rand_idx(dist.cols)
        precinct = dist.grid[row,col]
        neighbors = dist.get_neighbors(precinct)
        for neighbor in neighbors:

            # pick a neighbor with a different district id
            if neighbor.district_id != precinct.district_id:

                # create a proposed districting as if we were to flip this precinct with the neighbor
                proposed_dist = Districting(copy(dist.grid))
                proposed_dist.flip(precinct, neighbor)

                # apply the flip to the original districting if the proposed districting is valid
                if proposed_dist.is_valid():
                    dist.flip(precinct, neighbor)
                    break
    return dist, dist.get_efficiency_gap()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the gerrymandering simulator on an nxn grid')
    parser.add_argument('-s', '--steps', required=True, type=int, help='Number of steps to take for the random walk')
    parser.add_argument('-n', '--num-simulations', required=True, type=int, help='Number of simulations to run')
    parser.add_argument('-f', '--file', required=True, type=str, help="JSON file representing the grid to simulate on")

    args = parser.parse_args()
    main(args.steps,args.num_simulations,args.file)
