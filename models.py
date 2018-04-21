from collections import defaultdict

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
        self.n = grid.shape[0]

    def __str__(self):
        s = ''
        for row in range(self.n):
            for col in range(self.n):
                s += str(self.grid[row][col]) + '\n'
        return s

    def get_neighbors(self,row,col):
        """
        Get all (non-diagonal) neighbors for a given precinct

        Args:
            row (int): index for the row of the precinct
            col (int): index for the column of the precinct
        """
        neighbors = []

        if row-1 >= 0:
            neighbors.append(self.grid[row-1,col])
        if row+1 < self.n:
            neighbors.append(self.grid[row+1,col])
        if col-1 >= 0:
            neighbors.append(self.grid[row, col-1])
        if col+1 < self.n:
            neighbors.append(self.grid[row,col+1])

        return neighbors
