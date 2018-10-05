import math
import puzzle_globals

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
#
class State:
    # standard init function for the class with all the needed params
    def __init__(self, puz, cost, parent):
        self.puz = puz
        self.cost = cost
        self.parent = parent

    # check whether this state is a goal state or not
    def is_goal(self):
        if self.puz == puzzle_globals.GOAL:
            return true
        else:
            return false

    # function that returns all the possible moves that can be done from this State
    # as a list of states
    def expand(self):
        des = []
        total_rows = total_cols = math.sqrt(len(self.puz))
        # looks for the empty space
        # this will be used to deptermine the tiles that can be moved and where (index of 0)
        blank_index = self.puz.index(0)
        # TODO: push new states to des for every tile that be moved arround the blank tile
