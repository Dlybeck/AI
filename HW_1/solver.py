import math

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
        #print(total_moves)





    def __init__(self, puzzle_state):
        self.puzzle_state = puzzle_state

        self.height = len(self.puzzle_state)  # Number of rows
        self.width = len(self.puzzle_state[0])  # Number of columns

        self.move = None  # the move that is chosen to do based on the heuristic
        self.goal = [([None]*self.width)] * self.height #initialize empty array of correct size
        self.heuristic = self.find_heuristic()  # Call the method correctly
        self.create_goal() #set goal


puzzle = State([[6, 5, 2, 3], [5, 7, 11, 4], [9, 1, 10, 8], [15, 14, 13, 12]])
#print(puzzle.goal)




