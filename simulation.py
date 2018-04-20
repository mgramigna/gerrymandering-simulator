import models
import random
import math
import numpy as np
from uuid import uuid4

pick_rand_idx = lambda n: int(math.floor(random.random()*n))

def main():
    pass

def simulate(length, dist):
    dists = []
    for i in range(length):
        row, col = pick_rand_idx(dist.n), pick_rand_idx(dist.n)
        precinct = dist.grid[row,col]
        neighbors = dist.get_neighbors(row,col)



if __name__ == "__main__":
    main()
