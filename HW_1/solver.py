import math
import heapq
import copy

class State: 
    def find_heuristic(self):
        total_moves = 0
        for i in range(self.height):
            for j in range(self.width):
                if(self.puzzle_state[i][j] != 0): #skip the "empty" tile
                    tile_moves = 0
                    #find proper row and column index for current state
                    row_index = (self.puzzle_state[i][j] - 1) % self.width
                    column_index = math.floor((self.puzzle_state[i][j] - 1) / self.height)

                    #horizontal distance
                    tile_moves=abs(row_index - j)

                    #vertical distance
                    tile_moves += abs(column_index - i)

                    total_moves += tile_moves
                    #print(self.puzzle_state[i][j], "should move ", tile_moves, " [", row_index, "][", column_index, "]")  
                else:
                     self.holeY = i #set the coords of the hole
                     self.holeX = j
        #print(total_moves)
        return total_moves

    def __hash__(self):
        return hash(str(self.puzzle_state))

    def __init__(self, puzzle_state):
        self.holeY = None
        self.holeX = None
        self.move = None  #the move that is used to get to this state
        self.lastState = None
        self.moves = 0

        self.puzzle_state = puzzle_state
        self.height = len(self.puzzle_state)  # Number of rows
        self.width = len(self.puzzle_state[0])  # Number of columns
        self.heuristic = self.find_heuristic()  # Call the method correctly


    #Change the comparable for heapq
    def __lt__(self, nxt): 
        return self.heuristic < nxt.heuristic

def nextState(oldState, tileX, tileY):
    adjustedState = []
    adjustedState = copy.deepcopy(oldState.puzzle_state)
    tile = adjustedState[tileY][tileX]

    adjustedState[oldState.holeY][oldState.holeX] = tile #move tile to the empty place
    adjustedState[tileY][tileX] = 0 #put empty spot where tile was

    return State(adjustedState)
    

def containsState(newState, list):
    for state in list:
        if(state.puzzle_state == newState.puzzle_state): #if the state is in the closed list already
            return True
    return False

def getNextStates(state, closedlist = []):
    #get all of the potential states with 1 move
    allStates = []
    #Can move up
    if(state.holeY < (state.height-1)):
        #create new state with the tiles moved up
        newState = nextState(state, state.holeX, state.holeY+1)
        if(not containsState(newState, closedlist)):
            newState.move = 'U'
            newState.moves = state.moves + 1
            newState.heuristic += newState.moves
            newState.lastState = state
            allStates.append(newState)

    #Can move down
    if(state.holeY > 0):
        newState = nextState(state, state.holeX, state.holeY-1)
        if(not containsState(newState, closedlist)):
            newState.move = 'D'
            newState.moves = state.moves + 1
            newState.heuristic += newState.moves
            newState.lastState = state
            allStates.append(newState)



    #Can move right
    if(state.holeX < (state.width-1)):
        newState = nextState(state, state.holeX+1, state.holeY)
        if(not containsState(newState, closedlist)):
            newState.move = 'L'
            newState.moves = state.moves + 1
            newState.heuristic += newState.moves
            newState.lastState = state
            allStates.append(newState)


    #Can move left
    if(state.holeX > 0):
        newState = nextState(state, state.holeX-1, state.holeY)
        newState.move = 'R'
        newState.moves = state.moves + 1
        newState.heuristic += newState.moves
        newState.lastState = state
        allStates.append(newState)

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
    openlist = []
    closedlist = []
    runs = 0

    currentState = State(start)
    goal = create_goal(currentState)

    while((runs == 0 or len(openlist)!=0) and currentState.puzzle_state!=goal):
        runs += 1
        closedlist.append(currentState) #add currentState to the closedlist
        nextStates = getNextStates(currentState, closedlist)
        for i in range(len(nextStates)):
            heapq.heappush(openlist, nextStates[i]) #push each new state to the openlist

        #pick the next state
        newState = heapq.heappop(openlist)
        currentState = newState #update currentState for repeat

    #add final state to the closed list
    closedlist.append(currentState)

    # Trace back the path
    usedState = closedlist[-1]

    path = []
    path.append(usedState.move)
    # runs on all but the start state
    while (usedState.lastState):
        usedState = usedState.lastState
        if(usedState.lastState is not None):
            path.append(usedState.move)
    path.reverse()  # Reverse the list in-place
    return path
    

'''puzzle = [[1, 2, 3], [4, 5, 6], [7, 0, 8,]]
print("Original: ", puzzle)

print(solve(puzzle))'''