import math
import heapq
import copy

class State: 
    def create_goal(self):
        tile_num = 1
        for i in range(self.height):
            row = []  #variable for the current row
            for j in range(self.width):
                row.append(tile_num)  #add proper values to each row
                tile_num += 1
            self.goal[i] = row  #Append the new row to the goal

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
        self.move = None  # the move that is used to get to this state

        self.puzzle_state = puzzle_state
        self.height = len(self.puzzle_state)  # Number of rows
        self.width = len(self.puzzle_state[0])  # Number of columns
        self.goal = [([None]*self.width)] * self.height #initialize empty array of correct size
        self.heuristic = self.find_heuristic()  # Call the method correctly
        self.create_goal() #set goal

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
    



def getNextStates(state):
    #get all of the potential states with 1 move
    allStates = []
    #Can move up
    if(state.holeY < (state.height-1)):
        #create new state with the tiles moved up
        newState = nextState(state, state.holeX, state.holeY+1)
        newState.move = 'U'
        allStates.append(newState)

    #Can move down
    if(state.holeY > 0):
        newState = nextState(state, state.holeX, state.holeY-1)
        newState.move = 'D'
        allStates.append(newState)

    #Can move right
    if(state.holeX < (state.width-1)):
        newState = nextState(state, state.holeX+1, state.holeY)
        newState.move = 'R'
        allStates.append(newState)

    #Can move left
    if(state.holeX > 0):
        newState = nextState(state, state.holeX-1, state.holeY)
        newState.move = 'L'
        allStates.append(newState)

    return allStates


def solve(start):
    openlist = []
    closedlist = []

    currentState = State(start)
    heapq.heappush(openList, currentState)

    while(len(openlist)!=0 and currentState.heuristic != 0):
        closedlist.append(currentState) #add currentState to the closedlist
        nextStates = getNextStates(currentState)
        for i in range(len(nextStates)):
            heapq.heappush(openlist, nextStates[i]) #push each new state to the openlist

        #pick a new currentState
        currentState = heapq.heappop(openlist)

    #add final state to the closed list
    closedlist.append(currentState)

    #track back closed list and find all relevant moves
    currentHeuristic = 0
    reversePath = []
    for state in reversed(closedlist):
        if(state.heuristic > currentHeuristic):
            #since this state is not backtracking add it to the path
            reversePath.append(state.move)
            currentHeuristic = state.heuristic
    
    #reverse the path to get answer
    path = reversed(path)
    return path
        



print("Original: ", puzzle.puzzle_state)
swapped = getNextStates(puzzle)
print("Possible moves:")

heap = []
heapq.heappush(heap, puzzle)
for i in range(len(swapped)):
    heapq.heappush(heap, swapped[i])
    #print(swapped[i].puzzle_state)


for _ in range(len(heap)):
    puzzle = heapq.heappop(heap)
    print(puzzle.puzzle_state, " Heuristic: ", puzzle.heuristic)
