"""
This Connect Four player just picks a random spot to play. It's pretty dumb.
"""
__author__ = "Adam A. Smith" # replace my name with yours
__license__ = "MIT"
__date__ = "February 2018"

import random
import time

class ComputerPlayer:
    def __init__(self, id, difficulty_level):
        """
        Constructor, takes a difficulty level (likely the # of plies to look
        ahead), and a player ID that's either 1 or 2 that tells the player what
        its number is.
        """
        self.id = id

        self.depth = difficulty_level

        self.width = None
        self.height = None

        pass

    class State:
        def __init__(self, score, col_Index):
            self.score = score
            self.move = col_Index

    def pick_move(self, rack):
        """
        Pick the move to make. It will be passed a rack with the current board
        layout, column-major. A 0 indicates no token is there, and 1 or 2
        indicate discs from the two players. Column 0 is on the left, and row 0 
        is on the bottom. It must return an int indicating in which column to 
        drop a disc. The player current just pauses for half a second (for 
        effect), and then chooses a random valid move.
        """
        time_start = time.time()
        rack = [list(col) for col in rack]

        self.width = len(rack)
        self.height = len(rack[0])

        move = self.negamax(rack, self.id, self.depth)
        #print("Playing move with score ", -move.score)

        time_end = time.time()
        print("Finished move in ", time_end - time_start, " seconds")
        return move.move


    def negamax(self, rack, id, depth):
        if depth == 0 or self.Is_Game_Over(rack):
            return self.State(-self.evaluate(rack, id), None)

        best_State = self.State(-float('inf'), None)  # Initialize best_State with a very low score
        scores = []
        for col in range(self.width):
            for disc in range(self.height):
                # Can play here
                if rack[col][disc] == 0:
                    rack[col][disc] = id  # Make the move

                    # Recurse
                    new_State = self.negamax(rack, 3 - id, depth - 1)

                    scores.append(new_State.score)
                    # If this move is better than a previous move, update best_State
                    if new_State.score > best_State.score:
                        best_State.score = new_State.score
                        best_State.move = col

                    rack[col][disc] = 0  # Reset the move to make the next move
                    break  # To only look at one move per column
        #if(id == self.id): print("Bot picked ", best_State.score, " out of ", scores)
        #if(id != self.id): print("Player picked ", best_State.score, " out of ", scores)
        
        return self.State(-best_State.score, best_State.move)



    def Is_Game_Over(self, rack):
        full = True

        for col in range(self.width):
            if(rack[col][self.height-1] == 0): full = False
        return full

    def evaluate(self, rack, id):
        looked_at = 0
        total_score = 0
        #Check all horizontal quartets
        for col in range(self.width-3):
            for slot in range(self.height):
                looked_at += 1
                quartet = (rack[col][slot], rack[col+1][slot], rack[col+2][slot], rack[col+3][slot])
                total_score += self.Score_Quartet(quartet, id)
        #check for all the vertical quartets
        for col in range(self.width):
            for slot in range(self.height-3):
                looked_at += 1
                quartet = (rack[col][slot], rack[col][slot+1], rack[col][slot+2], rack[col][slot+3])
                total_score += self.Score_Quartet(quartet, id)
        #check low to high diagonals
        for col in range(self.width-3):
            for slot in range(self.height-3):
                looked_at += 1
                quartet = (rack[col][slot], rack[col+1][slot+1], rack[col+2][slot+2], rack[col+3][slot+3])
                total_score += self.Score_Quartet(quartet, id)
        #check high to low diagonals
        for col in range(self.width-3):
            for slot in range(self.height-3):
                slot +=3
                looked_at += 1
                quartet = (rack[col][slot], rack[col+1][slot-1], rack[col+2][slot-2], rack[col+3][slot-3])
                total_score += self.Score_Quartet(quartet, id)
        return total_score

    def Score_Quartet(self, quartet, id):
        whos_quartet = 0 #variable to keep track of what player has the first disc in this quarted
        count = 0
        for i in range(len(quartet)):
            #what player's discs are in this quartet?
            if(whos_quartet == 0 and quartet[i] != 0):
                whos_quartet = quartet[i]

            #There is nothing in this quartet
            if(quartet[i] == 0): continue
            #There is only one color in this quartet
            elif(quartet[i] == whos_quartet):
                count += 1
            #there is a mix of discs in this quartet
            else:
                count = 0
                break
        if(count != 0 and whos_quartet != 0):
            if(whos_quartet == id):
                #Positive
                if(count == 1): return 1
                elif(count == 2): return 10
                elif(count == 3): return 100
                else: return 1000000
            else:
                #negative
                if(count == 1): return -1
                elif(count == 2): return -10
                elif(count == 3): return -100
                else: return -1000000
                
        else:
            return 0