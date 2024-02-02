class State:
    
    def create_goal(self):
        tile_num = 1
        for i in range(self.height):
            row = []  #variable for the current row
            for j in range(self.width):
                row.append(tile_num)  #add proper values to each row
                tile_num += 1
            self.goal[i] = row  #Append the new row to the goal



    def __init__(self, puzzle_state):
        self.puzzle_state = puzzle_state

        self.height = len(self.puzzle_state)  # Number of rows
        self.width = len(self.puzzle_state[0])  # Number of columns

        #self.heuristic = self.find_heuristic()  # Call the method correctly
        self.move = None  # the move that is chosen to do based on the heuristic
        self.goal = [([None]*self.width)] * self.height #initialize empty array of correct size
        self.create_goal() #set goal


puzzle = State([[2, 2, 3], [4, 5, 6], [7, 8, 9]])
print(puzzle.goal)




