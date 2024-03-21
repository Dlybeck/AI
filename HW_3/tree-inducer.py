import sys
import math

class node:
    def __init__(self):
        next_Yea = None #if there is another node for yea, link here
        yea = None #label for yea if this is a leaf
        
        next_Nay = None
        nay = None
        
        next_Other = None
        other = None
    
class rep:
    def __init__(self, id, label, votes):
        self.id = id
        self.label = label
        self.votes = votes
        
    def __str__ (self):
        return self.id + " "+ self.label + " " + self.votes
  
def parse_arguments():
    #print("This is the name of the script: ", sys.argv[0])
    #print("Number of arguments: ", len(sys.argv))
    #print("The arguments are: " , str(sys.argv))
    
    if (len(sys.argv) > 2):
        print("Too many arguments given");
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
        reps[i] = rep(info[0], info[1], info[2])
        #print(reps[i])
    
    return reps
    
def split_data(data):
    tuning_set = []
    training_set = []
    for i in range(len(data)):
        if(i % 4 == 0): tuning_set.append(data[i]) #Create tuning set
        else: training_set.append(data[i]) #create training set
        
    return training_set, tuning_set

def log(num):
    if(num == 0):
        return -0
    else: return math.log(num, 2)

def calculate_entropy(subset):
    length = len(subset)
    if length == 0:
        return 0

    num_D = 0
    for rep in subset:
        if rep.label == 'D':
            num_D += 1
    num_R = length - num_D

    prob_D = num_D / length
    prob_R = num_R / length
    return -(prob_D*log(prob_D) + prob_R*log(prob_R))

def create_decision_tree(training_set):
    numA = 0
    numB = 0
    for rep in training_set:
        if(rep.label == 'D'): numA += 1
        else: numB += 1
    #print("There are ", numA, " Democrats and ", numB, " Republicans")
    
    #make it a probability not a total
    probA = numA/len(training_set)
    probB = numB/len(training_set)
    
    set_entropy = -((probA)*log(probA) + (probB)*log(probB))

    info_gain = 0
    max_info_gain = 0
    max_info_index = None
    entropy = 0
    y_entropy = 0
    n_entropy = 0
    o_entropy = 0
    
    #for each vote listed
    for i in range(len(training_set[0].votes)):
        yeas = []
        nays = []
        others = []

        #split up by vote
        for rep in training_set:
            #tally votes for this issue
            if(rep.votes[i] == '+'): yeas.append(rep)
            elif(rep.votes[i] == '-'): nays.append(rep)
            else: others.append(rep)

        #print("For issue ", chr(ord('A') + i), " there were ", len(yeas), " +'s, ", len(nays), " -'s and ", len(others), " abstains")
        
        #find probability of each vote
        probY = len(yeas)/len(training_set)
        probN = len(nays)/len(training_set)
        probO = len(others)/len(training_set)
        
        #entropy per vote
        y_entropy = calculate_entropy(yeas)
        n_entropy = calculate_entropy(nays)
        o_entropy = calculate_entropy(others)

        #total information gain
        info_gain = set_entropy - (probY*y_entropy + probN*n_entropy + probO*o_entropy)
        
        #print("     information gain is ", info_gain)
        
        #adjust max entropy
        if(info_gain > max_info_gain): 
            max_info_gain = info_gain
            max_info_index = i
        
    print("Max information gain is ", max_info_gain, " at issue ", chr(ord('A') + max_info_index))
        
        

if __name__ == "__main__":
    data = parse_arguments()
    training_set, tuning_set = split_data(data)
    create_decision_tree(training_set)
    
