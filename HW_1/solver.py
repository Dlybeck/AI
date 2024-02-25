import math
import heapq
import copy
import time

class Info:
    def __init__(self, puzzle_state, move, last_state):
        self.puzzle_state = puzzle_state
        self.move = move
        self.last_state = last_state

    def __hash__(self):
        return hash(str(self.puzzle_state))

    def __eq__(self, other):
        return self.puzzle_state == other.puzzle_state

class State:
    def __init__(self, puzzle_state):
        self.hole_y = None
        self.hole_x = None
        self.info = Info(puzzle_state, None, None)
        self.moves = 0
        self.heuristic = find_heuristic(self)

    def __lt__(self, other):
        return self.heuristic < other.heuristic

def find_heuristic(state):
    '''
    Finds a heuristic for a given state using the manhattan distance for each tile
    returns the heuristic as an int
    '''
    global goal_state
    total_moves = 0
    if goal_state is None:
        goal_state = create_goal_state(state)
    for i in range(height):
        for j in range(width):
            if (state.info.puzzle_state[i][j] != 0):
                goal_coords = find_tile(goal_state, state.info.puzzle_state[i][j])
                total_moves += abs(goal_coords[0] - i) + abs(goal_coords[1] - j)
            else:
                state.hole_y = i
                state.hole_x = j
    return total_moves

def find_tile(state, tile):
    for i in range(height):
        for j in range(width):
            if (state[i][j] == tile):
                return i, j

def check_puzzle_solvable(state):
    '''
    Checks if the puzzle is solveable
    Returns a boolean
    '''
    list = []
    inversions = 0
    gap = height - 1
    zeroFound = False
    #flatten the list puzzle
    for row in state.info.puzzle_state:
        for elem in row:
            if (elem != 0): list.append(elem)
            else: zeroFound = True
        if (zeroFound is False): gap -= 1
            
    #count the inversions
    for num in range(len(list)):
        i = num + 1
        while (i < len(list)):
            if (list[i] < list[num]): inversions += 1
            i += 1

    if (width % 2 == 0):
        sum = gap + inversions
        if (sum % 2 == 0): return True
        else: return False
    else:
        if (inversions % 2 == 0): return True
        else: return False

def create_next_position(old_state, tile_x, tile_y):
    '''
    Creates a new state with the hole in a new spot
    returns a state
    '''
    new_state = copy.deepcopy(old_state.info.puzzle_state)
    tile = new_state[tile_y][tile_x]
    new_state[old_state.hole_y][old_state.hole_x] = tile
    new_state[tile_y][tile_x] = 0
    return new_state

def update_state(state_list, state, new_pos, move, closed_set):
    '''
    Update all of the needed info for the new state
    '''
    info = Info(new_pos, move, state)
    if (info not in closed_set):
        new_state = State(new_pos)
        new_state.info.move = move
        new_state.moves = state.moves + 1
        new_state.heuristic += new_state.moves
        new_state.info.last_state = state
        state_list.append(new_state)

def get_next_states(state, closed_set):
    '''
    finds all the possible moves for a given states makes them as a state
    returns a list of states
    '''
    next_states = []
    if (state.hole_y < height - 1):
        new_pos = create_next_position(state, state.hole_x, state.hole_y + 1)
        update_state(next_states, state, new_pos, 'U', closed_set)
    if (state.hole_y > 0):
        new_pos = create_next_position(state, state.hole_x, state.hole_y - 1)
        update_state(next_states, state, new_pos, 'D', closed_set)
    if (state.hole_x < width - 1):
        new_pos = create_next_position(state, state.hole_x + 1, state.hole_y)
        update_state(next_states, state, new_pos, 'L', closed_set)
    if (state.hole_x > 0):
        new_pos = create_next_position(state, state.hole_x - 1, state.hole_y)
        update_state(next_states, state, new_pos, 'R', closed_set)
    return next_states

def create_goal_state(state):
    '''
    Given a state it creates the solution state
    returns a 2d array represening the final state
    '''
    goal = [[0] * width for _ in range(height)]
    num = 1
    for i in range(height):
        for j in range(width):
            goal[i][j] = num
            num += 1
    goal[height - 1][width - 1] = 0
    return goal

def solve(start):
    '''
    Given a 2d array of the current puzzle find the moves needed to solve the puzzle
    returns a list of the moves needed to solve
    '''
    start_time = time.time()
    global width, height, goal_state
    goal_state = None
    width = len(start[0])
    height = len(start)
    open_list = []
    closed_set = set()
    path = []

    start_state = State(start)

    if not check_puzzle_solvable(start_state):
        raise Exception("This puzzle is not solvable")

    heapq.heappush(open_list, start_state)
    goal_state = create_goal_state(start_state)

    while open_list:
        current_state = heapq.heappop(open_list)
        if current_state.info.puzzle_state == goal_state:
            break
        closed_set.add(current_state.info)
        next_states = get_next_states(current_state, closed_set)
        for next_state in next_states:
            heapq.heappush(open_list, next_state)

    path.append(current_state.info.move)
    while current_state.info.last_state:
        current_state = current_state.info.last_state
        if current_state.info.last_state:
            path.append(current_state.info.move)
    path.reverse()

    end_time = time.time()
    print("Completed in ", end_time - start_time, " seconds")
    return path


    #solve([[1, 2, 3], [4, 5, 6], [7, '.', 8]])