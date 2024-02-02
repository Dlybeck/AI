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

    def __hash__(self):
        return hash(str(self.puzzle_state))

    def __init__(self, puzzle_state):
        self.holeY = None
        self.holeX = None
        self.move = None  # the move that is chosen to do based on the heuristic

        self.puzzle_state = puzzle_state
        self.height = len(self.puzzle_state)  # Number of rows
        self.width = len(self.puzzle_state[0])  # Number of columns
        self.goal = [([None]*self.width)] * self.height #initialize empty array of correct size
        self.heuristic = self.find_heuristic()  # Call the method correctly
        self.create_goal() #set goal

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
        allStates.append(nextState(state, state.holeX, state.holeY+1))

    #Can move down
    if(state.holeY > 0):
        allStates.append(nextState(state, state.holeX, state.holeY-1))

    #Can move right
    if(state.holeX < (state.width-1)):
        allStates.append(nextState(state, state.holeX+1, state.holeY))

    #Can move left
    if(state.holeX > 0):
        allStates.append(nextState(state, state.holeX-1, state.holeY))

    return allStates


def solve(start):
    openlist = []
    closedlist = []

    #create a state for each possible move with neighbors


puzzle = State([[6, 5, 2, 3], [7, 0, 11, 4], [9, 1, 10, 8], [15, 14, 13, 12]])

print("Original: ", puzzle.puzzle_state)
swapped = getNextStates(puzzle)
print("Possible moves:")
for i in range(len(swapped)):
    print(swapped[i].puzzle_state)

