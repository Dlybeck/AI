import sys
import math

class Node:
    def __init__(self, issue=None):
        self.issue_to_split = issue #issue for this node

        #Children Nodes
        self.next_Yea = None
        self.next_Nay = None
        self.next_Other = None

        #Parent Node
        self.parent = None

        #if this node is a leaf, R or D?
        self.classification = None
    
    def print_node(self, level=0):
        if self.issue_to_split is not None:
            print("Issue "+chr(ord('A')+self.issue_to_split)+":")
        else:
            print(self.classification)
            return

        level = level + 1
        indent = " " * level * 2

        if self.next_Yea is not None:
            print(f"{indent}+", end=" ")
            self.next_Yea.print_node(level)
        if self.next_Nay is not None:
            print(f"{indent}-", end=" ")
            self.next_Nay.print_node(level)
        if self.next_Other is not None:
            print(f"{indent}.", end=" ")
            self.next_Other.print_node(level)
 
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
        global num_issues
        num_issues = len(info[2])
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

def classify(subset, node):
    num_D = 0
    for rep in subset:
        if rep.label == 'D':
            num_D += 1

    num_R = len(subset) - num_D

    if num_D > num_R:
        node.classification = 'D'
    elif num_R > num_D:
        node.classification = 'R'
    else:
        node.classification = node.parent.classification


def create_decision_tree(training_set, checked=set(), parent_node=None):
    #Count the D's and R's in this set
    num_D = 0
    for rep in training_set:
        if rep.label == 'D':
            num_D += 1
    num_R = len(training_set) - num_D

    #Base Case
    if (len(checked) == num_issues): #Loops thorugh and classifies based on parent if needed
        node = Node()
        node.parent = parent_node
        classify(training_set, node)
        return node
    elif(num_D == 0 or num_R == 0): #Doesn't loop through and classify when it already knows
        node = Node()
        node.parent = parent_node
        if(num_D == 0): node.classification = 'R'
        else: node.classification = 'D'
        return node
         
    #Entropy of entire set
    set_entropy = calculate_entropy(training_set)

    max_info_gain = 0
    max_info_index = None

    #Check information gain for each issue
    for i in range(num_issues):
        #Skip issue if already used to split data
        if i in checked:
            continue

        yeas, nays, others = split_by_vote(training_set, i)

        info_gain = set_entropy - (
                len(yeas) / len(training_set) * calculate_entropy(yeas) +
                len(nays) / len(training_set) * calculate_entropy(nays) +
                len(others) / len(training_set) * calculate_entropy(others)
        )

        #update info if a better split is found
        if (info_gain > max_info_gain):
            max_info_gain = info_gain
            max_info_index = i

    checked.add(max_info_index)
    node = Node(max_info_index)
    node.parent = parent_node
    classify(training_set, node)

    #If there is an issue left to split
    if max_info_index is not None:
        #Create a subset for each vote
        yeas, nays, others = split_by_vote(training_set, max_info_index)
        #Recurse
        node.next_Yea = create_decision_tree(yeas, checked.copy(), node)
        node.next_Nay = create_decision_tree(nays, checked.copy(), node)
        node.next_Other = create_decision_tree(others, checked.copy(), node)

    return node

def calculate_entropy(subset):
    num_D = sum(1 for rep in subset if rep.label == 'D')
    num_R = len(subset) - num_D
    total = len(subset)

    #if subset is empty 0 entropy
    if total == 0:
        return 0

    prob_D = num_D / total
    prob_R = num_R / total

    #if all R or D 0 entropy
    if prob_D == 0 or prob_R == 0:
        return 0

    #Return Entropy
    return -(prob_D * log(prob_D) + prob_R * log(prob_R))

def split_by_vote(subset, index):
    yeas = []
    nays = []
    others = []

    for rep in subset:
        if(rep.votes[index] == '+'):
            yeas.append(rep)
        elif (rep.votes[index] == '-'):
            nays.append(rep)
        else:
            others.append(rep)

    return yeas, nays, others
        

if __name__ == "__main__":
    data = parse_arguments()
    training_set, tuning_set = split_data(data)
    tree = create_decision_tree(training_set)
    tree.print_node()

    
