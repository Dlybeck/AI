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
                else:
                     self.holeY = i #set the coords of the hole
                     self.holeX = j
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
    
    def __eq__(self, other):
        return self.puzzle_state == other.puzzle_state

def checkPuzzle(state):
    list = []
    inversions = 0
    gap = state.height - 1
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

    if(state.width % 2 == 0):
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
    adjustedState = []
    adjustedState = copy.deepcopy(oldState.puzzle_state)
    tile = adjustedState[tileY][tileX]

    adjustedState[oldState.holeY][oldState.holeX] = tile #move tile to the empty place
    adjustedState[tileY][tileX] = 0 #put empty spot where tile was

    return State(adjustedState)

def getNextStates(state, closedlist):
    #get all of the potential states with 1 move
    allStates = []
    #Can move up
    if(state.holeY < (state.height-1)):
        #create new state with the tiles moved up
        newState = nextState(state, state.holeX, state.holeY+1)
        if(newState not in closedlist):
            newState.move = 'U'
            newState.moves = state.moves + 1
            newState.heuristic += newState.moves
            newState.lastState = state
            allStates.append(newState)

    #Can move down
    if(state.holeY > 0):
        newState = nextState(state, state.holeX, state.holeY-1)
        if(newState not in closedlist):
            newState.move = 'D'
            newState.moves = state.moves + 1
            newState.heuristic += newState.moves
            newState.lastState = state
            allStates.append(newState)



    #Can move right
    if(state.holeX < (state.width-1)):
        newState = nextState(state, state.holeX+1, state.holeY)
        if(newState not in closedlist):
            newState.move = 'L'
            newState.moves = state.moves + 1
            newState.heuristic += newState.moves
            newState.lastState = state
            allStates.append(newState)


    #Can move left
    if(state.holeX > 0):
        newState = nextState(state, state.holeX-1, state.holeY)
        if(newState not in closedlist):
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
    closedset = set()

    currentState = State(start)

    #Make sure puzzle is solveable
    if(checkPuzzle(currentState) == False):
        raise Exception("This puzzle is not solveable")
        return []
    heapq.heappush(openlist, currentState)
    goal = create_goal(currentState)

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
    return path
    

'''puzzle = [[6, 5, 2, 3], [0, 7, 11, 4], [9, 1, 10, 8], [15, 14, 13, 12]]
state = State(puzzle)'''