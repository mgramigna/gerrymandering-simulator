import random
import math
import argparse
import json
import numpy as np
from uuid import uuid4
from copy import copy
from models import Districting, Precinct

# Picks a random integer between 0 and n-1
pick_rand_idx = lambda n: int(math.floor(random.random()*n))

def main(n, step_length, trials, filepath):
    """
    Read in a user-defined districting and run the simulation

    Args:
        n (int): dimension of the grid
        step_length (str): number of `flips` to do for the grid
        trials (int): number of separate simulations to run for this grid
        filepath (str): path to the json file specifying the districting
    """
    grid = np.empty(shape=(n,n), dtype=Precinct)
    with open(filepath) as f:
        data = json.load(f)

    if len(data) != n:
        print 'ERROR: Provided json file does not match the specified dimension'
        return

    row,col = (0,0)
    for d in data:
        if len(d) != n:
            print 'ERROR: Provided json file does not match the specified dimension'
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

    print 'Original Districting\n---------------\n\n', dist

    for t in range(trials):
        old,new,result = simulate(step_length, dist)
        print 'Resulting Districting\n---------------\n\n', result

def simulate(length, dist):
    """
    Run a random walk for a given districting and determine the differing party counts

    Args:
        length (int): number of steps to take in the walk
        dist (numpy.ndarray): original districting before the simulation

    Returns:
    """

    # get party voting counts before the simulatinos
    old_party_count = dist.get_party_count()
    for i in range(length):

        # pick a random cell in the grid
        row, col = pick_rand_idx(dist.n), pick_rand_idx(dist.n)
        precinct = dist.grid[row,col]
        neighbors = dist.get_neighbors(precinct)
        for neighbor in neighbors:

            # pick a neighbor with a different district id
            if neighbor.district_id != precinct.district_id:

                # create a proposed districting as if we were to flip this precinct with the neighbor
                proposed_dist = Districting(copy(dist.grid))
                proposed_dist.grid[row,col] = Precinct(precinct.party, neighbor.district_id)

                # apply the flip to the original districting if the proposed districting is valid
                if proposed_dist.is_valid():
                    dist.flip(precinct, neighbor, row, col)
                    break
    return old_party_count, dist.get_party_count(), dist

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the gerrymandering simulator on an nxn grid')
    parser.add_argument('-d', '--dimension', required=True, type=int, help='Dimension of the grid (integer)')
    parser.add_argument('-s', '--steps', required=True, type=int, help='Number of steps to take for the random walk')
    parser.add_argument('-n', '--num-simulations', required=True, type=int, help='Number of simulations to run')
    parser.add_argument('-f', '--file', required=True, type=str, help="JSON file representing the grid to simulate on")

    args = parser.parse_args()
    main(args.dimension,args.steps,args.num_simulations,args.file)
