import math
import heapq
import copy
import time

class State: 
    def __init__(self, puzzle_state):
        self.holeY = None
        self.holeX = None
        self.move = None  #the move that is used to get to this state
        self.lastState = None
        self.moves = 0
        self.puzzle_state = puzzle_state
        self.height = len(self.puzzle_state)  # Number of rows
        self.width = len(self.puzzle_state[0])  # Number of columns
        self.heuristic = None

    def __hash__(self):
        return hash(str(self.puzzle_state))

    #Change the comparable for heapq
    def __lt__(self, nxt): 
        return self.heuristic < nxt.heuristic
    
    def __eq__(self, other):
        return self.puzzle_state == other.puzzle_state

def find_heuristic(state):
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

def checkHeuristicChange(oldX, oldY, x, y, oldState):
    #old num of moves to correct position
    num = oldState.puzzle_state[oldY][oldX]
    row_index = (num-1) % oldState.width
    column_index = (num-1) // oldState.height
    tile_moves1=abs(row_index - oldX) #horizontal distance
    tile_moves1 += abs(column_index - oldY) #vertical distance

    #new num of moves to the correct position
    num = oldState.puzzle_state[y][x]
    row_index = (num-1) % oldState.width
    column_index = (num-1) // oldState.height
    tile_moves2=abs(row_index - x) #horizontal distance
    tile_moves2 += abs(column_index - y) #vertical distance

    return tile_moves2 - tile_moves1


def updateHeuristic(state):
    oldState = state.lastState
    heuristic = oldState.heuristic
    change = 0

    if(state.move == 'U'):
        state.holeY = oldState.holeY + 1
        state.holeX = oldState.holeX
        change = checkHeuristicChange(oldState.holeX, oldState.holeY+1, oldState.holeX, oldState.holeY, oldState)
    elif(state.move == 'D'):
        state.holeY = oldState.holeY - 1
        state.holeX = oldState.holeX
        change = checkHeuristicChange(oldState.holeX, oldState.holeY-1, oldState.holeX, oldState.holeY, oldState)
    elif(state.move == 'L'):
        state.holeX = oldState.holeX + 1
        state.holeY = oldState.holeY
        change = checkHeuristicChange(oldState.holeX, oldState.holeY, oldState.holeX+1, oldState.holeY, oldState)
    elif(state.move == 'R'):
        state.holeX = oldState.holeX - 1
        state.holeY = oldState.holeY
        change = checkHeuristicChange(oldState.holeX, oldState.holeY, oldState.holeX-1, oldState.holeY, oldState)
    
    heuristic += change
    return heuristic
    

def checkPuzzle(state):
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

def nextState(oldState, tileX, tileY):
    adjustedState = []
    adjustedState = copy.deepcopy(oldState.puzzle_state)
    tile = adjustedState[tileY][tileX]

    adjustedState[oldState.holeY][oldState.holeX] = tile #move tile to the empty place
    adjustedState[tileY][tileX] = 0 #put empty spot where tile was

    return State(adjustedState)

def createState(stateList, state, newState, move, closedSet):
    if newState not in closedSet:
        newState.move = move
        newState.moves = state.moves + 1
        newState.lastState = state
        newState.heuristic = updateHeuristic(newState)
        newState.heuristic += newState.moves
        stateList.append(newState)

#get all of the potential states with 1 move
def getNextStates(state, closedSet):
    allStates = []
    #Can move up
    if state.holeY < (state.height-1):
        #create new state with the tiles moved up
        newState = nextState(state, state.holeX, state.holeY+1)
        createState(allStates, state, newState, 'U', closedSet)
    #Can move down
    if state.holeY > 0:
        newState = nextState(state, state.holeX, state.holeY-1)
        createState(allStates, state, newState, 'D', closedSet)
    #Can move right
    if state.holeX < (state.width-1):
        newState = nextState(state, state.holeX+1, state.holeY)
        createState(allStates, state, newState, 'L', closedSet)
    #Can move left
    if state.holeX > 0:
        newState = nextState(state, state.holeX-1, state.holeY)
        createState(allStates, state, newState, 'R', closedSet)
    return allStates

def create_goal(state):
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
    startTime = time.time()
    openlist = []
    closedset = set()
    path = []
    currentState = State(start)
    currentState.heuristic = find_heuristic(currentState)

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
    print("Completed in ", endTime - startTime, " seconds")

    return path