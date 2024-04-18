import sys

'''
This class is used to hold all of a representatives data such as their id, what their label is
and their voting history
'''
class rep:
    def __init__(self, id, label, coords):
        self.id = id
        self.label = label
        self.coords = coords
        
    def __str__ (self):
        coord_Str = ""
        for coord in self.coords:
            coord_Str += ' '+str(coord)
        return self.id + " "+ self.label + " " + coord_Str

'''
Parses through the arguments given from the command line and turns the given data into a list of reps

Return: a list of reps
'''
def parse_arguments(): 
    if (len(sys.argv) > 3 or len(sys.argv)< 3):
        print("ERROR: Incorrect Number of Arguments")
        print("Usage: python <file> <num of groups>")
        sys.exit()
    
    fileName = sys.argv[1]
    
    try:
        file = open(fileName, 'r')
    except FileNotFoundError:
        print("This file does not exist")
    

    repStrings = file.readlines()
    
    #process each individual line now and turn them into rep objects
    reps = [None]*len(repStrings)
    
    for i in range(len(repStrings)):
        #Split up string into parts
        info = repStrings[i].split()
        global num_issues
        num_issues = len(info[2])

        votes = info[2]

        coords = []

        for vote in votes:
            if vote == '+': coords.append(1)
            elif vote == '-': coords.append(-1)
            elif vote == '.': coords.append(0)
            else:
                print("ERROR: Invalid vote: -", vote, "-")
                sys.exit()




        reps[i] = rep(info[0], info[1], coords)

    return reps

def find_Distance(rep1, rep2):
    coords1 = rep1.coords
    coords2 = rep2.coords

    distance = 0
    for i in range(len(coords1)):
        distance += abs(coords1[i] - coords2[i])

    return distance

'''
Main method
'''
if __name__ == "__main__":
    data = parse_arguments()
    print(data[0])

    distance = find_Distance(data[0], data[1])
    print(distance)
