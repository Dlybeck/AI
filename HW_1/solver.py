import math
import heapq
import copy
import time

height = None
width = None

class State: 
    def __hash__(self):
        return hash(tuple(map(tuple, self.puzzle_state)))
    
    def __init__(self, puzzle_state):
        '''
        Initialize state
        '''
        self.holeY = None
        self.holeX = None
        self.info = Info(puzzle_state, None, None)
        self.moves = 0

        self.puzzle_state = puzzle_state
        self.heuristic = None


    #Change the comparable for heapq
    def __lt__(self, other): 
        return self.heuristic < other.heuristic
    
    def __eq__(self, other):
        return self.puzzle_state == other.puzzle_state

def find_heuristic(state):
        total_moves = 0
        for i in range(height):
            for j in range(width):
                if(state.puzzle_state[i][j] != 0): #skip the "empty" tile
                    tile_moves = 0
                    #find proper row and column index for current state
                    row_index = (state.puzzle_state[i][j] - 1) % width
                    column_index = math.floor((state.puzzle_state[i][j] - 1) / height)

                    #horizontal distance
                    tile_moves=abs(row_index - j)

                    #vertical distance
                    tile_moves += abs(column_index - i)

                    total_moves += tile_moves
                else:
                     state.holeY = i #set the coords of the hole
                     state.holeX = j
        return total_moves

def checkPuzzle(state):
    '''
    Checks if the puzzle is solveable
    Returns a boolean
    '''
    lst = []
    inversions = 0
    gap = height - 1
    zeroFound = False

    #flatten the list puzzle
    for row in state.info.puzzle_state:
        for elem in row:
            if elem != 0: lst.append(elem)
            else: zeroFound = True
        if not zeroFound: gap -= 1
        
    #count the inversions
    for num in range(len(lst)):
        i = num + 1
        while i < len(lst):
            if lst[i] < lst[num]: inversions += 1
            i += 1

    if(width % 2 == 0):
        sum = gap+inversions
        if(sum % 2 == 0):
            return True
        else:
            return False
    else:
        if inversions % 2 == 0: return True
        else: return False

def createNextPosition(oldState, tileX, tileY):
    '''
    copies the old state and makes a new one with a moved tile
    returns the new state
    '''
    adjustedState = []
    for row in oldState.info.puzzle_state:
        copiedRow = list(row)
        adjustedState.append(copiedRow)
    
    tile = adjustedState[tileY][tileX]
    adjustedState[oldState.holeY][oldState.holeX] = tile  # move tile to the empty place
    adjustedState[tileY][tileX] = 0  # put empty spot where tile was

    return State(adjustedState)

def updateState(newState, oldState, move, allStates, closedSet):
    if(newState not in closedSet):
        newState.move = move
        newState.moves = oldState.moves + 1
        newState.heuristic = find_heuristic(newState)
        newState.heuristic += newState.moves
        newState.lastState = oldState
        allStates.append(newState)
    

def getNextStates(state, closedSet):
    #get all of the potential states with 1 move
    allStates = []
    
    #Can move up
    if(state.holeY < (height-1)):
        #create new state with the tiles moved up
        newState = nextState(state, state.holeX, state.holeY+1)
        updateState(newState, state, 'U', allStates, closedSet)
    #Can move down
    if(state.holeY > 0):
        newState = nextState(state, state.holeX, state.holeY-1)
        updateState(newState, state, 'D', allStates, closedSet)
    #Can move right
    if(state.holeX < (width-1)):
        newState = nextState(state, state.holeX+1, state.holeY)
        updateState(newState, state, 'L', allStates, closedSet)
    #Can move left
    if(state.holeX > 0):
        newState = nextState(state, state.holeX-1, state.holeY)
        updateState(newState, state, 'R', allStates, closedSet)
    return allStates

def create_goal(height, width):
    '''
    Creates a 2d array of the solved state for the heuristic to compare to
    '''
    goal = []
    tile_num = 1
    for i in range(height):
        row = []
        for j in range(width):
            row.append(tile_num)
            tile_num += 1
        goal.append(row)
    goal[height - 1][width - 1] = 0  # set last tile to be empty
    return goal

def solve(start):
    startTime = time.time()
    openlist = []
    closedset = set()

    global height
    global width
    height = len(start)
    width = len(start[0])

    #Initialize the heuristic
    currentState = State(start)
    currentState.heuristic = find_heuristic(currentState)

    # Make sure puzzle is solveable
    if not checkPuzzle(currentState):
        raise Exception("This puzzle is not solveable")
    
    heapq.heappush(openlist, currentState)
    goal = create_goal(height, width)

    while openlist and currentState.info.puzzle_state != goal:
        newState = heapq.heappop(openlist)  # pick the next state
        currentState = newState  # update currentState for repeat
        closedset.add(currentState.info)  # add currentState to the closedset
        nextStates = getNextStates(currentState, closedset)
        for nextState in nextStates:
            heapq.heappush(openlist, nextState)  # push each new state to the openlist

    closedset.add(currentState.info)  # add final state to the closed set
    path.append(currentState.info.move)  # Trace back the path
    
    # runs on all but the start state
    while currentState.info.lastState:
        currentState = currentState.info.lastState
        if currentState.info.lastState is not None:
            path.append(currentState.info.move)
    path.reverse()  # Reverse the list in-place
    
    endTime = time.time()
    print("Completed in ",endTime - startTime," seconds")
    return path