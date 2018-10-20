import sys
import random

from state import *
from queue import PriorityQueue
from puzzle_globals import Globals

# n puzzle misplaced tiles heuristic
# returns the sum of all the misplaced tiles in the state compared to goal in
#   puzzle_globals.py
def h_misplaced_tiles(state):
    res = 0
    for tiles_index in range(len(state.puz)):
        if state.puz[tiles_index] != Globals.GOAL[tiles_index]:
            res += 1
    return res

# n puzzle manhattan distance heuristic
# returns the sum of manhattan distance of all the tiles in the state compared to goal in
#   puzzle_globals.py
def h_manhattan_distance(state):
    if len(state.puz) != len(Globals.GOAL):
        raise Exception('state puzzle length is not equal to goal length')

    res = 0
    total_rows = total_cols = int(math.sqrt(len(state.puz)))

    for state_index in range(len(state.puz)):

        goal_index = Globals.GOAL.index(state.puz[state_index])

        state_row = state_index // total_cols
        state_col = state_index % total_cols

        goal_row = goal_index // total_cols
        goal_col = goal_index % total_cols

        res += abs(state_row - goal_row) + abs(state_col - goal_col)

    return res



# function to do a search from an initial state and
# returns a dictionary {solution : [solution states],
#                        max_frontier_size : int, states_eval : int}
def do_search(init_state,ignore_dups = False):
    res = {
        'solutions' : [],
        'max_frontier_size' : 0,
        'states_evaluated' : 0,
    }
    frontier = PriorityQueue()
    frontier.put(init_state)

    duplicates = {}

    while( not frontier.empty()):
        curr_state = frontier.get(False)

        res['states_evaluated'] += 1
        if curr_state.is_goal():
            res['solutions'].append(curr_state)
            return res

        else:
            children = curr_state.expand()

            for child in children:
                if not str(child.puz) in duplicates and ignore_dups:
                    duplicates[str(child.puz)] = 1
                    frontier.put(child)
                elif not ignore_dups:
                    frontier.put(child)

            res['max_frontier_size'] = max(res['max_frontier_size'],frontier.qsize())
    return res

# creates a random solvable config of the puzzle
# inputs : the goal array
def shuffle_puzzle(goal):
    n_moves = random.randint(1,100)
    res = list(goal)
    for n_moves in range(n_moves):
        blank_index = res.index(0)
        # do random move
        tile_index = random.choice(get_movable_tiles(res))
        res[blank_index], res[tile_index] = res[tile_index], res[blank_index]

    return res


def get_movable_tiles(puzzle):
    movable_tiles = []
    total_rows = total_cols = int(math.sqrt(len(puzzle)))
    # looks for the empty space
    # this will be used to deptermine the tiles that can be moved and where (index of 0)
    blank_index = puzzle.index(0)
    # calculate the row and col on a '2D' list from a 1D list
    blank_row = blank_index // total_cols
    blank_col = blank_index % total_cols

    # list of movable tiles (around the blank tile - top , left, bottom, right)
    # each item in the list is the ordered pair of row and col for each tile
    tiles = [   [blank_row - 1, blank_col], # top
                [blank_row, blank_col - 1], # left
                [blank_row + 1, blank_col], # bottom
                [blank_row, blank_col + 1]] # right
    
    for tile in tiles:
        # check if the movable tile is inside the grid
        if  tile[0] >= 0 and tile[0] < total_rows and \
            tile[1] >= 0 and tile[1] < total_cols:
            # calculate actual index of the tile in a one dimensional list
            actual_index = tile[0] * total_cols + tile[1]
            movable_tiles.append(actual_index)

    return movable_tiles

def main():
    initial_state = State([1,2,3,4,0,5,6,7,8], 0, None)
    out = do_search(initial_state,ignore_dups = True)
    print(str(out))
    print(str(out['solutions'][0].cost))

if __name__ == '__main__':
    main()
