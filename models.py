class Precinct(object):
    def __init__(self, party, district_id):
        self.party = party
        self.district_id = district_id
    def __str__(self):
        return "District: %s; Party: %s" % (self.district_id, self.party)

class Districting(object):
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
