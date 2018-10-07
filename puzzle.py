import sys

from state import *
from Queue import PriorityQueue
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

        state_row = state_index / total_cols
        state_col = state_index % total_cols

        goal_row = goal_index / total_cols
        goal_col = goal_index % total_cols

        res += abs(state_row - goal_row) + abs(state_col - goal_col)

    return res



# function to do a blind search (UCS) from an initial state and
# returns a dictionary {solution : [solution states],
#                        max_frontier_size : int, states_eval : int}
# TODO: replace exhaustive to limit of solutions
def do_search(init_state,exhaustive = False):
    res = {
        'solution' : [],
        'max_frontier_size' : 0,
        'states_evaluated' : 0
    }
    frontier = PriorityQueue()
    frontier.put(init_state)

    while( not frontier.empty()):
        curr_state = frontier.get(False)
        print str(curr_state) + "\n" + str(frontier.qsize())

        res['states_evaluated'] += 1
        if curr_state.is_goal():
            res['solution'].append(curr_state)
            if not exhaustive:
                return res
        else:
            children = curr_state.expand()

            for child in children:
                frontier.put(child)

            res['max_frontier_size'] = max(res['max_frontier_size'],frontier.qsize())
    return res

def main():
    initial_state = State([1,0,2,3,4,5,6,7,8],0,None)
    out = do_blind_search(initial_state)
    print out

if __name__ == '__main__':
    main()
