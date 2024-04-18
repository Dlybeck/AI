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
    if(int(sys.argv[2]) < 2):
        print("ERROR: Number of groups must be 2 or greater")
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

    return reps, int(sys.argv[2])

def find_farthest_nodes(reps, n):
    distances = []
    for i in range(len(reps)):
        for j in range(i + 1, len(reps)):
            rep1 = reps[i]
            rep2 = reps[j]
            if rep1 != rep2:  # Skip duplicate pairs
                distance = find_Distance(rep1, rep2)
                distances.append((distance, (rep1, rep2)))

    # Sort distances in descending order using a custom selection sort algorithm
    for i in range(n):
        max_index = i
        for j in range(i + 1, len(distances)):
            if distances[j][0] > distances[max_index][0]:
                max_index = j
        distances[i], distances[max_index] = distances[max_index], distances[i]

    # Select the farthest nodes without duplicates
    farthest_nodes = []
    seen_nodes = set()
    for distance, (rep1, rep2) in distances:
        if rep1 not in seen_nodes and rep2 not in seen_nodes:
            farthest_nodes.append((distance, (rep1, rep2)))
            seen_nodes.add(rep1)
            seen_nodes.add(rep2)
            if len(farthest_nodes) == n:
                break
    
    max_Reps = []
    i = 0
    while(len(max_Reps) < n):
        max_Reps.append(farthest_nodes[i][1][0])

        if(len(max_Reps) < n):
            max_Reps.append(farthest_nodes[i][1][1])

        i += 1



    return max_Reps



def find_Distance(rep1, rep2):
    coords1 = rep1.coords
    coords2 = rep2.coords

    squared_Dists = []
    for i in range(len(coords1)):
        squared_Dists.append((coords1[i] - coords2[i]) ** 2)
    return sum(squared_Dists)

'''
Main method
'''
if __name__ == "__main__":
    data, n = parse_arguments()

    maxReps = find_farthest_nodes(data, n)

    for rep in maxReps:
        print(rep)
    
