import math
import heapq
import copy
import time

height = None
width = None

class State: 
    def __hash__(self):
        '''
        makes it so State can be properly hashed
        '''
        return hash(tuple(map(tuple, self.puzzle_state)))
    
    def __init__(self, puzzle_state):
        '''
        Initialize State
        '''
        self.holeY = None
        self.holeX = None
        self.move = None  #the move that is used to get to this state
        self.lastState = None
        self.moves = 0

        self.puzzle_state = puzzle_state
        self.heuristic = None


    #Change the comparable for heapq
    def __lt__(self, other): 
        '''
        makes the States sorted properly in the heapq
        '''
        return self.heuristic < other.heuristic
    
    def __eq__(self, other):
        '''
        makes the state properly compareable
        '''
        return self.puzzle_state == other.puzzle_state

def find_heuristic(state):
    '''
    Given a state it finds the estimated number of moves needed to solve the puzzle
    '''
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
    Takes a state and checks that it is actually solveable. Returns true if it is false if not
    '''
    list = []
    inversions = 0
    gap = height - 1
    zeroFound = False
    #flatten the list puzzle
    for row in state.puzzle_state:
        for elem in row:
            if(elem != 0):
                list.append(elem)
            else:
                zeroFound = True
        if(zeroFound == False):
            gap -= 1
    #count the inversions
    for num in range(len(list)):
        i = num + 1
        while(i < len(list)):
            if(list[i] < list[num]):
                inversions += 1
            i += 1
            
    if(width % 2 == 0):
        sum = gap+inversions
        if(sum % 2 == 0):
            return True
        else:
            return False
    else:
        if(inversions % 2 == 0):
            return True
        else:
            return False



def nextState(oldState, tileX, tileY):
    '''
    creates a state one move away from the old state
    '''
    adjustedState = []
    adjustedState = copy.deepcopy(oldState.puzzle_state)
    tile = adjustedState[tileY][tileX]

    adjustedState[oldState.holeY][oldState.holeX] = tile #move tile to the empty place
    adjustedState[tileY][tileX] = 0 #put empty spot where tile was

    return State(adjustedState)

def updateState(newState, oldState, move, allStates, closedSet):
    '''
    if the state has not already been looked at, update all of the needed info for it
    '''
    if(newState not in closedSet):
        newState.move = move
        newState.moves = oldState.moves + 1
        newState.heuristic = find_heuristic(newState)
        newState.heuristic += newState.moves
        newState.lastState = oldState
        allStates.append(newState)
    

def getNextStates(state, closedSet):
    '''
    Takes a state and the closed set. Creates all possible next moves from the current state. Returns a list of all possible next states
    '''
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

def create_goal():
    '''
    creates a 2d array of the solved puzzle to compare to
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
    '''
    Takes a 2d array representing the puzzle and returns an array of the moves needed to solve the puzzle
    '''
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

    #Make sure puzzle is solveable
    if(checkPuzzle(currentState) == False):
        raise Exception("This puzzle is not solveable")
        return []
    heapq.heappush(openlist, currentState)
    goal = create_goal()
    print(goal)

    while len(openlist) != 0 and currentState.puzzle_state != goal:
        newState = heapq.heappop(openlist)  # pick the next state
        currentState = newState  # update currentState for repeat

        closedset.add(currentState)  # add currentState to the closedset
        nextStates = getNextStates(currentState, closedset)
        for i in range(len(nextStates)):
            heapq.heappush(openlist, nextStates[i])  # push each new state to the openlist

    print("Past first loop")
    # add final state to the closed set
    closedset.add(currentState)
    # Trace back the path
    path = []
    path.append(currentState.move)
    # runs on all but the start state
    while currentState.lastState:
        currentState = currentState.lastState
        if currentState.lastState is not None:
            path.append(currentState.move)
    path.reverse()  # Reverse the list in-place
    
    endTime = time.time()
    print("Completed in ",endTime - startTime," seconds")
    return path