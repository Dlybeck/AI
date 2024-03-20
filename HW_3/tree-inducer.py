import sys
import math

class rep:
    def __init__(self, id, label, votes):
        self.id = id
        self.label = label
        self.votes = votes
        
    def __str__ (self):
        return self.id + " "+ self.label + " " + self.votes
  
def parse_arguments():
    print("This is the name of the script: ", sys.argv[0])
    print("Number of arguments: ", len(sys.argv))
    print("The arguments are: " , str(sys.argv))
    
    if (len(sys.argv) > 2):
        print("Too many arguments given");
        sys.exit
    
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
        print(reps[i])
    
    return reps
    
def split_data(data):
    tuning_set = []
    training_set = []
    for i in range(len(data)):
        if(i % 4 == 0): tuning_set.append(data[i]) #Create tuning set
        else: training_set.append(data[i]) #create training set
        
    return training_set, tuning_set

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
    
    set_entropy = (-probA)*math.log2(probA) + (-probB)*math.log2(probB)

    current_info = 0
    max_info = 0
    current_entropy = 0
    #for each vote listed
    for i in range(len(training_set[0].votes)):
        y = 0
        n = 0
        other = 0
        for rep in training_set:
            #tally votes for this issue
            if(rep.votes[i] == '+'): y += 1
            elif(rep.votes[i] == '-'): n += 1
            else: other += 1
        #print("For issue ", i, " there were ", y, " +'s, ", n, " -'s and ", other, " abstains")
        
        
        probY = y/len(training_set)
        probN = n/len(training_set)
        probOther = other/len(training_set)
        
        current_entropy = (-probY)*math.log2(probY) + (-probN)*math.log2(probN) + (-probOther)*math.log2(probOther)
        current_info = set_entropy - current_entropy
        
        #adjust max entropy
        if(current_entropy > max_entropy): max_entropy = current_entropy
        
        

if __name__ == "__main__":
    data = parse_arguments()
    training_set, tuning_set = split_data(data)
    create_decision_tree(training_set)
    
