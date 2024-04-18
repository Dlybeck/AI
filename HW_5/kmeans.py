import sys
import copy
'''
This class is used to hold all of a representatives data such as their id, what their label is
and their voting history
'''
class rep:
    def __init__(self, id, label, coords):
        self.id = id
        self.label = label
        self.coords = coords
        self.group = -1
        
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

def find_Start(reps, n):
    distances = []
    for i in range(len(reps)):
        for j in range(i + 1, len(reps)):
            rep1 = reps[i]
            rep2 = reps[j]
            if rep1 != rep2:  # Skip duplicates
                distance = find_Distance(rep1.coords, rep2.coords)
                distances.append((distance, (rep1, rep2)))

    #Sort distances by distance (x[0])
    sorted_distances = sorted(distances, key=lambda x: x[0], reverse=True)

    # Select the farthest nodes without duplicates
    farthest_reps = []
    seen_reps = set()
    for distance, (rep1, rep2) in sorted_distances:
        if rep1 not in seen_reps and rep2 not in seen_reps:
            farthest_reps.append((distance, (rep1, rep2)))
            seen_reps.add(rep1)
            seen_reps.add(rep2)
            if len(farthest_reps) == n:
                break

    max_coords = []
    max_reps = []
    i = 0
    while (i < len(farthest_reps)) and len(max_coords) < n:
        distance, (rep1, rep2) = farthest_reps[i]
        if rep1.coords not in max_coords:
            max_coords.append(rep1.coords)
            max_reps.append(rep1.id)
        if rep2.coords not in max_coords and len(max_coords) < n:
            max_coords.append(rep2.coords)
            max_reps.append(rep2.id)
        i += 1

    print()
    print("Initial centroids based on: ", ', '.join(max_reps))

    return max_coords

def find_Distance(coords1, coords2):
    squared_Dists = []
    for i in range(len(coords1)):
        squared_Dists.append((coords1[i] - coords2[i]) ** 2)
    return sum(squared_Dists)

def E_Step(data, centroids):
    #for every point
    for rep in data:
        #find the best classification
        best_Dist = None
        group = 0
        for cent in centroids:
            dist = find_Distance(rep.coords, cent)
            if(best_Dist == None) or (dist < best_Dist):
                best_Dist = dist
                rep.group = group

            group += 1

#Move centroids to center of group
def M_Step(data, centroids):
    # num of reps in each group (initialized to 0)
    group_Sizes = [0] * len(centroids)
    group_Sums = []
    for i in range(len(centroids)):
        group_Sums.append([0] * len(centroids[0]))

    for rep in data:
        group_Sizes[rep.group] += 1
        for i in range(len(rep.coords)):
            group_Sums[rep.group][i] += rep.coords[i]

    # Update the centroids with the new centroid positions
    for i in range(len(group_Sizes)):
        if group_Sizes[i] > 0:
            centroids[i] = [num / group_Sizes[i] for num in group_Sums[i]]
        else:
            centroids[i] = [0] * len(centroids[i])


def sameData(data1, data2):
    for i in range(len(data1)):
        if(data1[i].group != data2[i].group): return False
    return True



'''
Main method
'''
if __name__ == "__main__":
    data, n = parse_arguments()

    centroids = find_Start(data, n)
    old_Centroids = []
    rounds = 0
    while(old_Centroids != centroids):
        rounds+=1
        old_Centroids = copy.deepcopy(centroids)
        E_Step(data, centroids)
        M_Step(data, centroids)
    
    print("Converged after ", rounds, " rounds of k-means.")
    for i in range(len(centroids)):
        size = 0
        Ds = 0
        Rs = 0

        for rep in data:
            if(rep.group == i):
                if(rep.group == i): size+=1
                if(rep.label == 'D'): Ds+=1
                if(rep.label == 'R'): Rs+=1

        Ds = (Ds/size)*100
        Rs = (Rs/size)*100
        print("   Group" + str(i+1)+ ":  size "+ str(size)+ " ("+ str(round(Ds, 3))+ "% D, "+ str(round(Rs, 3))+ "% R)")


    
    



    
