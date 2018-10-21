import sys
import random
import plotly
import plotly.graph_objs as go

from plotly import tools
from state import *
from queue import PriorityQueue
from puzzle_globals import Globals
from tqdm import tqdm

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

def plot(x_val, y_val, line_name):
    trace = go.Scatter(
        x = x_val,
        y = y_val,
        mode = 'lines',
        name = line_name
    )
    return trace;

# helper function to get the key data sorting
def get_key(l):
    return l[0]
def get_plotdata(name, data_set, heuristic_function=None, heuristic_only = False):
    res = {}
    solution_depth_array = []
    max_frontier_size_array = []
    num_of_nodes_visited_array = []
    # list of lists(l) of length 2 where l[0] is the solution detph and l[1] is the max_frontier_size
    space_complexity_points = []
    complexity_points = []
    optimality_points = []

    for x in tqdm(range(len(data_set)), desc = name):
        random_initial_config = data_set[x]
        goal_state = do_search(State(random_initial_config, 0, None, heuristic_function,heuristic_only), ignore_dups = True)
        complexity_points.append([ goal_state['solutions'][0].cost, goal_state['max_frontier_size'], goal_state['states_evaluated']])
        optimality_points.append([ x, goal_state['solutions'][0].cost ])

    complexity_points = sorted(complexity_points, key = get_key)

    solution_depth_array = [p[0] for p in complexity_points]
    max_frontier_size_array = [p[1] for p in complexity_points]
    num_of_nodes_visited_array = [p[2] for p in complexity_points]

    res['space_complexity_plot'] = plot(solution_depth_array,max_frontier_size_array,name) #for space complexity graph
    res['time_complexity_plot'] = plot(solution_depth_array,num_of_nodes_visited_array,name) # for time complexity graph
    res['optimality_plot'] = plot([ p[0] for p in optimality_points ],[ p[1] for p in optimality_points ],name) # for optimality graph

    return res

def main():
    sample_size = 25

    samples = [shuffle_puzzle(Globals.GOAL) for i in range(sample_size)]

    ucs_plotdata = get_plotdata(name = "UCS/BFS",data_set = samples)
    greedy_mt_plotdata = get_plotdata(name = "Greedy Best First Search - Misplaced Tiles Heuristic" , data_set = samples, heuristic_function = h_misplaced_tiles, heuristic_only = True)
    greedy_md_plotdata = get_plotdata(name = "Greedy Best First Search - Manhattan Distance Heuristic", data_set = samples, heuristic_function = h_manhattan_distance, heuristic_only = True)
    a_star_mt_plotdata = get_plotdata(name = "A* - Misplaced Tiles Heuristic", data_set = samples, heuristic_function = h_misplaced_tiles)
    a_star_md_plotdata = get_plotdata(name = "A* - Manhattan Distance Heuristic", data_set = samples, heuristic_function = h_manhattan_distance)

    space_complexity_data = [ucs_plotdata['space_complexity_plot'], \
        greedy_mt_plotdata['space_complexity_plot'], \
        greedy_md_plotdata['space_complexity_plot'], \
        a_star_mt_plotdata['space_complexity_plot'], \
        a_star_md_plotdata['space_complexity_plot'] ]

    time_complexity_data = [ucs_plotdata['time_complexity_plot'], \
        greedy_mt_plotdata['time_complexity_plot'], \
        greedy_md_plotdata['time_complexity_plot'], \
        a_star_mt_plotdata['time_complexity_plot'], \
        a_star_md_plotdata['time_complexity_plot'] ]

    optimality_data = [ucs_plotdata['optimality_plot'], \
        greedy_mt_plotdata['optimality_plot'], \
        greedy_md_plotdata['optimality_plot'], \
        a_star_mt_plotdata['optimality_plot'], \
        a_star_md_plotdata['optimality_plot'] ]

    plotly.offline.plot({
    "data": space_complexity_data,
    "layout": go.Layout(title="Space Complexity", xaxis={'title':"Solution Depth"}, yaxis={'title':"Max Frontier Size"})
    }, auto_open=True, filename='space-complexity.html')

    plotly.offline.plot({
    "data": time_complexity_data,
    "layout": go.Layout(title="Time Complexity", xaxis={'title':"Solution Depth"}, yaxis={'title':"States Evaluated"})
    }, auto_open=True, filename='time-complexity.html')

    plotly.offline.plot({
    "data": optimality_data,
    "layout": go.Layout(title="Optimality", xaxis={'title':"Instances"}, yaxis={'title':"Solution Depth"})
    }, auto_open=True, filename='optimality.html')

if __name__ == '__main__':
    main()
