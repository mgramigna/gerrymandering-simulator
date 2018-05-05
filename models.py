import random
import numpy as np
from uuid import uuid4
from collections import defaultdict

class Precinct(object):
    """
    Class representing an individual precinct within a districts

    Note:
        self.id is automatically generated when a new precinct is created

    Args:
        party (str): identifies the party that this precinct voted with
        district_id (str): the id of the district that this precinct is a party of
    """
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
        self.rows is assigned automatically based on the shape of the `grid` arg
        self.cols is assigned automatically based on the shape of the `grid` arg
        self.shape is assigned automatically for ease of use in further iterating of the grid

    Args:
        grid (numpy.ndarray): a 2d array of tuples for each precinct in a districting
    """
    def __init__(self, grid):
        self.grid = grid
        self.shape = grid.shape
        self.rows, self.cols = grid.shape

    def __str__(self):
        s = ''
        for row,col in np.ndindex(self.shape):
            s += str(self.grid[row][col])
            if col == self.cols-1:
                s += '\n'
        return s

    def get_neighbors(self,precinct):
        """
        Get all (non-diagonal) neighbors for a given precinct

        Args:
            precinct: the precinct whose neighbors we wish to find
        """
        neighbors = []
        row,col = self.__index_of(precinct)

        if row-1 >= 0:
            neighbors.append(self.grid[row-1,col])
        if row+1 < self.rows:
            neighbors.append(self.grid[row+1,col])
        if col-1 >= 0:
            neighbors.append(self.grid[row, col-1])
        if col+1 < self.cols:
            neighbors.append(self.grid[row,col+1])

        random.shuffle(neighbors)
        return neighbors

    def is_valid(self):
        """
        Tests if a given districting is valid (simply connected and has contiguous districts)

        Returns:
            bool: True if the districting is valid, False otherwise
        """
        return self.__is_contiguous() and self.__is_connected() and self.__is_population_valid()

    def flip(self,precinct,neighbor):
        """
        Absorb a given precinct into the neighboring district

        Args:
            precinct (Precinct): the precinct being absorbed
            neighbor (Precinct): the neighboring precinct in the district that is being absorbed
        """
        row,col = self.__index_of(precinct)
        self.grid[row,col] = Precinct(precinct.party, neighbor.district_id)

    def get_efficiency_gap(self):
        """
        Calculate the EG value for a given districting

        Note:
            See the referenced paper for the formula
        """
        district_votes = defaultdict(lambda: defaultdict(float))
        total_votes = defaultdict(float)
        wins = defaultdict(float)
        T = 0.0
        S = 0.0
        parties = set()

        for coords, p in np.ndenumerate(self.grid):
            district_votes[p.district_id][p.party] += 1.0
            total_votes[p.party] += 1.0
            parties.add(p.party)
            T += 1.0

        parties = tuple(parties)

        for d in district_votes:
            winner,_ = max(district_votes[d].items(), key=lambda x: x[1])
            wins[winner] += 1.0
            S += 1.0

        TA = total_votes[parties[0]]
        TB = total_votes[parties[1]]
        SA = wins[parties[0]]
        SB = wins[parties[1]]

        return ((TA-TB)/T) - (.5*((SA-SB)/S))

    def __is_contiguous(self):
        """
        Private function for testing if a grid contains contiguous districts

        Returns:
            bool: True if the number of contiguous precincts in the grid is equal to the number of total precincts, False otherwise
        """
        contiguous_precinct_count = 0
        for row,col in np.ndindex(self.shape):
            neighbors = self.get_neighbors(self.grid[row,col])
            for neighbor in neighbors:

                # if there is at least one neighbor with the same precinct, this precinct is contiguous
                if neighbor.district_id == self.grid[row,col].district_id:
                    contiguous_precinct_count += 1
                    break

        # all precincts should be contiguous
        return contiguous_precinct_count == self.rows*self.cols

    def __is_connected(self):
        """
        Private function for testing if the districts are simply connected

        Returns:
            bool: True if there are no breaks in the districts, False otherwise
        """

        # total number of precincts that fall under a given district
        precincts_per_district = defaultdict(lambda: defaultdict(int))

        # calculcate the expected number of precincts we should see for a given district
        for row,col in np.ndindex(self.shape):
            precincts_per_district[self.grid[row,col].district_id]['expected'] += 1

        searched_districts = set()
        for row,col in np.ndindex(self.shape):

            # don't search a district if we've already searched it before
            if self.grid[row,col].district_id in searched_districts:
                continue

            # start a depth first search from this point in the grid
            searcher = [self.grid[row,col]]
            current_district = self.grid[row,col].district_id

            # don't search this district in further iterations
            searched_districts.add(current_district)

            # find all neighbors with matching districts and mark them as seen
            seen = set()
            while len(searcher) > 0:
                precinct = searcher.pop()
                precincts_per_district[precinct.district_id]['seen'] += 1
                seen.add(precinct.id)
                neighbors = self.get_neighbors(precinct)
                nodes = []
                for n in neighbors:
                    if n.id not in seen and n.district_id == precinct.district_id:
                        seen.add(n.id)
                        nodes.append(n)
                searcher.extend(nodes)

            # after we process this district, we should have searched all precincts with that distrcits if the grid is connected
            if precincts_per_district[current_district]['seen'] != precincts_per_district[current_district]['expected']:
                return False
        return True

    def __is_population_valid(self):
        """
        Determine if the population spread is valid

        Note:
            This is pretty arbitrary, but right now I set no two districts to have a population difference greater than the number of rows plus the number of columns

        Returns:
            bool: True if the population spread is valid, false otherwise
        """
        populations = defaultdict(int)
        for _, precinct in np.ndenumerate(self.grid):
            populations[precinct.district_id] += 1

        ordered_populations = sorted(populations.items(), key=lambda p: p[1])
        max = ordered_populations[len(ordered_populations)-1][1]
        min = ordered_populations[0][1]

        return max - min <= self.rows+self.cols

    def __index_of(self, precinct):
        """
        Find the matching row and column for a given precinct

        Args:
            precinct (Precinct): the precinct to search for

        Returns:
            tuple: coordinates of the precinct of the form (row,col). (-1,-1) if not found
        """
        for row,col in np.ndindex(self.shape):
            if self.grid[row,col].id == precinct.id:
                return (row,col)
        return (-1,-1)
