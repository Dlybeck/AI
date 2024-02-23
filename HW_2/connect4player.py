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
        self.id = id
        self.depth = difficulty_level
        """
        Constructor, takes a difficulty level (likely the # of plies to look
        ahead), and a player ID that's either 1 or 2 that tells the player what
        its number is.
        """
        pass

    def pick_move(self, rack):
        """
        Pick the move to make. It will be passed a rack with the current board
        layout, column-major. A 0 indicates no token is there, and 1 or 2
        indicate discs from the two players. Column 0 is on the left, and row 0 
        is on the bottom. It must return an int indicating in which column to 
        drop a disc. The player current just pauses for half a second (for 
        effect), and then chooses a random valid move.
        """
        evaluate(rack);

    def evaluate(self, rack):
        looked_at = 0
        total_score = 0
        #Check all horizontal quartets
        for col in range(len(rack) - 3):
            for slot in range(len(rack[col])):
                looked_at += 1
                quartet = (rack[col][slot], rack[col+1][slot], rack[col+2][slot], rack[col+3][slot])
                total_score += self.Score_Quartet(quartet)

        print("Looked at ", looked_at, " quartets")

    def Score_Quartet(self, quartet):
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
            if(count == 0): return 0
            if(whos_quartet == self.id):
                #Positive
                if(count == 1): return 1
                elif(count == 2): return 10
                elif(count == 3): return 100
                else: return 100000
            else:
                #negative
                if(count == 1): return -1
                elif(count == 2): return -10
                elif(count == 3): return -100
                else: return -100000
        else:
            return 0

player = ComputerPlayer(1, 4)

player.evaluate([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])