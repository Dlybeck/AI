import sys

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
    
        


if __name__ == "__main__":
    data = parse_arguments()
    training_set, tuning_set = split_data(data)
    create_decision_tree(training_set)
    
