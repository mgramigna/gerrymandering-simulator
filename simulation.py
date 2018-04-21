import random
import math
import numpy as np
from uuid import uuid4
from models import Districting

# Picks a random integer between 0 and n-1
pick_rand_idx = lambda n: int(math.floor(random.random()*n))

def main(n, step_length):
    grid = np.empty(shape=(n,n), dtype=tuple)
    for row in range(n):
        dist_id = str(uuid4())
        for col in range(n):
            party = 'rep' if random.random() < .5 else 'dem'
            grid[row, col] = (party, dist_id)

    dist = Districting(grid)
    print simulate(step_length, dist)

def simulate(length, dist):
    """
    Run a random walk for a given districting and determine the differing party counts

    Args:
        length (int): number of steps to take in the walk
        dist (numpy.ndarray): original districting before the simulation
    """
    old_party_count = dist.get_party_count()
    for i in range(length):
        row, col = pick_rand_idx(dist.n), pick_rand_idx(dist.n)
        precinct = dist.grid[row,col]
        neighbors = dist.get_neighbors(row,col)
        for neighbor in neighbors:
            if neighbor[1] != precinct[1]:
                dist.grid[row,col] = (precinct[0], neighbor[1])
                break
    return old_party_count, dist.get_party_count()

if __name__ == "__main__":
    main(3, 3)
