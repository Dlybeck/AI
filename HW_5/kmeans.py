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
        return self.id + " "+ self.label + " " + self.votes

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

        cords = [num_issues]

        for vote in votes:
            if vote == '+': coords.append(1)
            if vote == '-': coords.append(-1)
            if vote == '.': coords.append(0)
            else:
                print("ERROR: Invalid vote")
                sys.exit()




        reps[i] = rep(info[0], info[1], info[2])

    return reps

'''
Main method
'''
if __name__ == "__main__":
    data = parse_arguments()
    print(data[0])