import math
from puzzle_globals import Globals

# This is the state representation for the n-puzzle problem
# puz is a one dimensional list of numbers
#   the numbers represent individual tiles
#   the length of the list is row * col where row = col = sqrt(n+1)
#   we use this so then it'll be easier to find the index of any tile in the list
#
# cost is the accumulated path cost to this state
#   cost = number of tiles moved (1)
#   this also means cost = depth
#
class State:
    # standard init function for the class with all the needed params
    def __init__(self, puz, cost, parent, heuristic_function = None, heuristic_only = False):
        # convert puz to a one dimensional list
        self.puz = puz
        self.cost = cost
        self.parent = parent
        self.heuristic_function = heuristic_function
        self.heuristic_only = heuristic_only

        if heuristic_function:
            self.heuristic = heuristic_function(self)
        else:
            self.heuristic = 0

    def __str__(self):
        total_rows = total_cols = int(math.sqrt(len(self.puz)))
        chunked = []
        for i in range(total_rows):
            temp = []
            for j in range(total_cols):
                temp.append(self.puz[i * total_cols + j])
            chunked.append(temp)

        str_out = ""
        for row in chunked:
            str_out += str(row) + "\n"

        return str_out + str(self.cost)

    def __cmp__(self, other):
        if self.heuristic_only:
            return self.heuristic - other.heuristic
        else:
            return (self.cost + self.heuristic) - (other.cost + other.heuristic)

    # check whether this state is a goal state or not
    def is_goal(self):
        if self.puz == Globals.GOAL:
            return True
        else:
            return False

    # function that returns all the possible moves that can be done from this State
    # as a list of states
    def expand(self):
        des = []
        total_rows = total_cols = int(math.sqrt(len(self.puz)))
        # looks for the empty space
        # this will be used to deptermine the tiles that can be moved and where (index of 0)
        blank_index = self.puz.index(0)
        # calculate the row and col on a '2D' list from a 1D list
        blank_row = blank_index / total_cols
        blank_col = blank_index % total_cols

        # list of movable tiles (around the blank tile - top , left, bottom, right)
        # each item in the list is the ordered pair of row and col for each tile
        movable_tiles =     [[blank_row - 1, blank_col], # top
                            [blank_row, blank_col - 1], # left
                            [blank_row + 1, blank_col], # bottom
                            [blank_row, blank_col + 1]] # right

        for tile in movable_tiles:
            # check if the movable tile is inside the grid
            if  tile[0] >= 0 and tile[0] < total_rows and \
                tile[1] >= 0 and tile[1] < total_cols:
                # calculate actual index of the tile in a one dimensional list
                actual_index = tile[0] * total_cols + tile[1]
                # clone list, so it doesnt affect the old list
                temp_list = list(self.puz)
                # swap the blank tiles
                # intermidiate variables
                a = blank_index
                b = actual_index
                temp_list[a], temp_list[b] = temp_list[b], temp_list[a]
                des.append(State(temp_list, self.cost + 1, self, self.heuristic_function,self.heuristic_only))
        return des
