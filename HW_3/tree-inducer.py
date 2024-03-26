import sys
import math
'''
This Program takes a file with representatives and their voting history.
It then creates a decision tree which can be used for future classification. 
It also has an accuracy check using leave one out validation

Author: David Lybeck
Date: 3/25/24
'''

'''
Node class represents one node in a decion tree, it can take in issue that it uses to split the data by
if no issue is given it just assumes it is a leaf
'''
class Node:
    '''
    Node constructor
    '''
    def __init__(self, issue=None):
        self.issue_to_split = issue #issue for this node

        #Children Nodes
        self.next_Yea = None
        self.next_Nay = None
        self.next_Other = None
        self.pruned = False

        #Parent Node
        self.parent = None

        #if this node is a leaf, R or D?
        self.classification = None
    
    '''
    Prints the node and all of its children in a tree format
    '''
    def print_node(self, level=0):
        if self.issue_to_split is not None or self.pruned:
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
 
'''
This class is used to hold all of a representatives data such as their id, what their label is
and their voting history
'''
class rep:
    def __init__(self, id, label, votes):
        self.id = id
        self.label = label
        self.votes = votes
        
    def __str__ (self):
        return self.id + " "+ self.label + " " + self.votes
  
'''
Parses through the arguments given from the command line and turns the given data into a list of reps

Return: a list of reps
'''
def parse_arguments():    
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

    return reps
    
'''
Splits a list of reps into a tuning set and a training set

Returns: Training set, Tuning set
'''
def split_data(data):
    tuning_set = []
    training_set = []
    for i in range(len(data)):
        if(i % 4 == 0): tuning_set.append(data[i]) #Create tuning set
        else: training_set.append(data[i]) #create training set
        
    return training_set, tuning_set

'''
This is used to repace math.log2. The only difference is that the log of 0 is set to be 0

Returns: answer to log
'''
def log(num):
    if(num == 0):
        return -0
    else: return math.log(num, 2)

'''
Calculates the entropy of a given set
Returns: entropy as num
'''
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



'''
Classifies a list of data based on the majority, or parent classification if it is tied
'''
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


'''
Creates a decision tree given a training set and a set() to keep track of checked issues
Return: the root node of the tree
'''
def create_decision_tree(training_set, checked, parent_node=None):
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

        #split by issue i
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

    checked.add(max_info_index) #mark that this issue is already been looked at
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

'''
Takes a set of reps and splits it into set of yeas nays and others
Resturn: List of yeas, list of nays, list of others
'''
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

'''
Predict the outcome of a given rep with a given decision tree
'''
def predict(rep, node):
    #base case
    if (node.issue_to_split == None or node.pruned): return node.classification

    vote = rep.votes[node.issue_to_split]

    #Recurse
    if (vote == '+'): return predict(rep, node.next_Yea)
    elif (vote == '-'): return predict(rep, node.next_Nay)
    else: return predict(rep, node.next_Other)

'''
Tests the accuracy of a tree using its tuning set as new data
'''
def test_accuracy(tree, tuning_set):
    correct = 0
    for rep in tuning_set:
        prediction = predict(rep, tree)
        if (prediction == rep.label):
            correct += 1
    return correct / len(tuning_set)

'''
Takes a tree and a tuning set, and finds the best node to potentially prune
Return: Node, Accuracy
'''
def reduced_error_pruning(tree, tuning_set, current_node=None, best_node=None, best_accuracy=-1):
    if current_node is None:
        current_node = tree

    if current_node.issue_to_split is None:
        return best_node, best_accuracy

    #Mark the current node and its children as pruned
    current_node.pruned = True

    new_accuracy = test_accuracy(tree, tuning_set)

    #Unmark the current node and its children as pruned
    current_node.pruned = False

    #Check to see if this is the best node to prune
    if new_accuracy >= best_accuracy:
        best_node = current_node
        best_accuracy = new_accuracy

    # Recurse on the children of the current node
    if current_node.next_Yea is not None:
        best_node, best_accuracy = reduced_error_pruning(tree, tuning_set, current_node.next_Yea, best_node, best_accuracy)
    if current_node.next_Nay is not None:
        best_node, best_accuracy = reduced_error_pruning(tree, tuning_set, current_node.next_Nay, best_node, best_accuracy)
    if current_node.next_Other is not None:
        best_node, best_accuracy = reduced_error_pruning(tree, tuning_set, current_node.next_Other, best_node, best_accuracy)

    return best_node, best_accuracy
          
'''
Remove all the modes marked to be pruned
'''
def trim(node):
    #Remove Children
    node.next_Yea = None
    node.next_Nay = None
    node.next_Other = None

    #Set this node to be a leaf node
    node.issue_to_split = None

'''
Given a tree and a tuning set, find if there are any nodes to prune off the tree and then remove
'''
def prune (tree, tuning_set):
    # Calculate initial accuracy
    accuracy = test_accuracy(tree, tuning_set)

    run = True
    while(run):
        #Find the best possible node to trim
        node_to_trim, new_accuracy = reduced_error_pruning(tree, tuning_set)
        #If this best option is an improvement, prune it
        if(new_accuracy >= accuracy and node_to_trim.parent is not None):
            node_to_trim.issue_to_split = None
            trim(node_to_trim)
            new_accuracy = accuracy
        #otherwise quit
        else:
            run = False

'''
Create a decision tree with the given data
Return: Root node of pruned tree
'''
def make_Tree (data):
    training_set, tuning_set = split_data(data)
    tree = create_decision_tree(training_set, set())
    prune(tree, tuning_set)
    return tree

'''
Given a set of data create a tree and use leave one out cross validation to find the overall accuracy
Return: Accuracy of decision tree
''' 
def LOOCV(data):
    correct = 0
    for i in range(len(data)):
        #create training set without element i in data
        training_set = data[:i] + data[i+1:]

        tree = make_Tree(training_set)

        #Predict the result of the skipped data
        prediction = predict(data[i], tree)

        #Count correct predections
        if prediction == data[i].label:
            correct += 1

    # Return the accuracy
    return correct / len(data)

'''
Main method
'''
if __name__ == "__main__":
    data = parse_arguments()
    
    tree = make_Tree(data)

    #Print pruned tree
    tree.print_node()

    #accuracy = test_accuracy(tree, data)
    #print("Accuracy of the decision tree after pruning: ", accuracy)

    accuracy = LOOCV(data)

    print("Accuracy is: ", accuracy)