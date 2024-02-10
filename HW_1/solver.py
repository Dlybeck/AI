import math
import heapq
import copy
import time

class State: 
    def __init__(self, puzzle_state):
        '''
        Initialize state
        '''
        self.holeY = None
        self.holeX = None
        self.move = None  #the move that is used to get to this state
        self.lastState = None
        self.moves = 0
        self.puzzle_state = puzzle_state
        self.height = len(self.puzzle_state)  # Number of rows
        self.width = len(self.puzzle_state[0])  # Number of columns
        self.heuristic = find_heuristic(self)  # Call the method correctly

    def __hash__(self):
        '''
        Proper hash function for state
        '''
        return hash(str(self.puzzle_state))

    def __lt__(self, nxt): 
        '''
        Update less than for the heapq comparison
        '''
        return self.heuristic < nxt.heuristic
    
    def __eq__(self, other):
        '''
        Makes the states compare properly
        '''
        return self.puzzle_state == other.puzzle_state

def find_heuristic(state):
    '''
    Finds the heuristic given a state
    returns the value of the heuristic
    '''
    total_moves = 0
    for i in range(state.height):
        for j in range(state.width):
            if state.puzzle_state[i][j] != 0: #skip the "empty" tile
                #find proper row and column index for current state
                row_index = (state.puzzle_state[i][j] - 1) % state.width
                column_index = math.floor((state.puzzle_state[i][j] - 1) / state.height)
                tile_moves=abs(row_index - j) #horizontal distance
                tile_moves += abs(column_index - i) #vertical distance
                total_moves += tile_moves
            else: #found the hole
                    state.holeY = i #set the coords of the hole
                    state.holeX = j
    return total_moves

def checkPuzzle(state):
    '''
    Checks if the puzzle is solveable
    Returns a boolean
    '''
    list = []
    inversions = 0
    gap = state.height - 1
    zeroFound = False

    #flatten the list puzzle
    for row in state.puzzle_state:
        for elem in row:
            if elem != 0: list.append(elem)
            else: zeroFound = True
        if zeroFound is False: gap -= 1
            
    #count the inversions
    for num in range(len(list)):
        i = num + 1
        while i < len(list):
            if list[i] < list[num]: inversions += 1
            i += 1

    if state.width % 2 == 0:
        sum = gap+inversions
        if sum % 2 == 0: return True
        else: return False
    else:
        if inversions % 2 == 0: return True
        else: return False

def createNextState(oldState, tileX, tileY):
    '''
    copies the old state and makes a new one with a moved tile
    returns the new state
    '''
    adjustedState = []
    adjustedState = copy.deepcopy(oldState.puzzle_state)
    tile = adjustedState[tileY][tileX]
    adjustedState[oldState.holeY][oldState.holeX] = tile #move tile to the empty place
    adjustedState[tileY][tileX] = 0 #put empty spot where tile was

    return State(adjustedState)

def updateState(stateList, state, newState, move, closedlist):
    '''
    updates all of the values if it hasn't already been explored
    '''
    if newState not in closedlist:
        newState.move = move
        newState.moves = state.moves + 1
        newState.heuristic += newState.moves
        newState.lastState = state
        stateList.append(newState)

#get all of the potential states with 1 move
def getNextStates(state, closedlist):
    '''
    creates states for every possible move
    returns a list of all the created states
    '''
    allStates = []
    #Can move up
    if state.holeY < (state.height-1):
        #create new state with the tiles moved up
        newState = createNextState(state, state.holeX, state.holeY+1)
        updateState(allStates, state, newState, 'U', closedlist)
    #Can move down
    if state.holeY > 0:
        newState = createNextState(state, state.holeX, state.holeY-1)
        updateState(allStates, state, newState, 'D', closedlist)
    #Can move right
    if state.holeX < (state.width-1):
        newState = createNextState(state, state.holeX+1, state.holeY)
        updateState(allStates, state, newState, 'L', closedlist)
    #Can move left
    if state.holeX > 0:
        newState = createNextState(state, state.holeX-1, state.holeY)
        updateState(allStates, state, newState, 'R', closedlist)
    return allStates

def create_goal(state):
    '''
    Creates a 2d array of the solved state for the heuristic to compare to
    '''
    goal = []
    tile_num = 1
    for i in range(state.height):
        row = []
        for j in range(state.width):
            row.append(tile_num)
            tile_num += 1
        goal.append(row)
    goal[state.height - 1][state.width - 1] = 0  # set last tile to be empty
    return goal

def solve(start):
    '''
    Takes a 2d array representing the current state of the puzzle and solves it
    Returning an array of moves needed to do to solve the puzzle
    '''
    startTime = time.time()

    openlist = []
    closedset = set()
    path = []
    currentState = State(start)

    #Make sure puzzle is solveable
    if checkPuzzle(currentState) is False: raise Exception("This puzzle is not solveable")
    
    heapq.heappush(openlist, currentState)
    goal = create_goal(currentState)

    while len(openlist) != 0 and currentState.puzzle_state != goal:
        newState = heapq.heappop(openlist)  # pick the next state
        currentState = newState  # update currentState for repeat
        closedset.add(currentState)  # add currentState to the closedset
        nextStates = getNextStates(currentState, closedset)
        for i in range(len(nextStates)): heapq.heappush(openlist, nextStates[i])  # push each new state to the openlist

    closedset.add(currentState) # add final state to the closed set
    path.append(currentState.move) # Trace back the path
    
    # runs on all but the start state
    while currentState.lastState:
        currentState = currentState.lastState
        if currentState.lastState is not None: path.append(currentState.move)
    path.reverse()  # Reverse the list in-place

    endTime = time.time()
    print("Completed in ", endTime-startTime, " seconds")
    return path