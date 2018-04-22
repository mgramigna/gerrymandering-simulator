import numpy as np
from uuid import uuid4
from collections import defaultdict

class Precinct(object):
    def __init__(self, party, district_id):
        self.id = str(uuid4())
        self.party = party
        self.district_id = district_id

    def __str__(self):
        return "%s,%s      " % (self.party,self.district_id)

class Districting(object):
    """
    Class representing a districting grid

    Note:
        self.n is assigned automatically based on the shape of the `grid` arg

    Args:
        grid (numpy.ndarray): a 2d array of tuples for each precinct in a districting
    """
    def __init__(self, grid):
        self.grid = grid
        self.shape = grid.shape
        self.n = grid.shape[0]

    def __str__(self):
        s = ''
        for row,col in np.ndindex(self.shape):
            s += str(self.grid[row][col])
            if col == self.n-1:
                s += '\n'
        return s

    def get_neighbors(self,precinct):
        """
        Get all (non-diagonal) neighbors for a given precinct

        Args:
            row (int): index for the row of the precinct
            col (int): index for the column of the precinct
        """
        neighbors = []
        row,col = self.__index_of(precinct)

        if row-1 >= 0:
            neighbors.append(self.grid[row-1,col])
        if row+1 < self.n:
            neighbors.append(self.grid[row+1,col])
        if col-1 >= 0:
            neighbors.append(self.grid[row, col-1])
        if col+1 < self.n:
            neighbors.append(self.grid[row,col+1])

        return neighbors

    def get_party_count(self):
        """
        Gets the number of precincts for each party in all districts
        """
        districts = defaultdict(lambda: defaultdict(int))

        for row,col in np.ndindex(self.shape):
            precinct = self.grid[row,col]
            districts[precinct.district_id][precinct.party] += 1

        return districts

    def is_valid(self):
        return self.__is_contiguous()

    def flip(self,precinct,neighbor,row,col):
        self.grid[row,col] = Precinct(precinct.party, neighbor.district_id)

    def __is_contiguous(self):
        contiguous_precinct_count = 0
        for row,col in np.ndindex(self.shape):
            neighbors = self.get_neighbors(self.grid[row,col])
            for neighbor in neighbors:
                if neighbor.district_id == self.grid[row,col].district_id:
                    contiguous_precinct_count += 1
                    break
        return contiguous_precinct_count == self.n**2
    def __index_of(self, precinct):
        for row,col in np.ndindex(self.shape):
            if self.grid[row,col].id == precinct.id:
                return (row,col)
        return (-1,-1)
