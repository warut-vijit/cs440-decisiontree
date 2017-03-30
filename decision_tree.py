import csv
from math import log

def load_csv():
    """Loads examples from a file into a dictionary of tuples"""
    with open('decision_tree.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        tree = [tuple(row) for row in csvreader]
        return tree

def split(arr, index):
    """Splits an array of example tuples by attribute at position index"""
    if all(isinstance(elmnt, tuple) for elmnt in arr):
        split_arr = {}
        for elmnt in arr:
            if elmnt[index] not in split_arr:
                split_arr[elmnt[index]] = [elmnt]
            else:
                split_arr[elmnt[index]].append(elmnt)
        return split_arr
    else:
        raise ValueError("Attempting to branch from non-leaf node")

def entropy(arr):
    """Computes the entropy of an array of example tuples"""
    if all(isinstance(elmnt, tuple) for elmnt in arr):
        labels = {}
        for elmnt in arr:
            if elmnt[-1] not in labels:
                labels[elmnt[-1]] = 1
            else:
                labels[elmnt[-1]] += 1
        for label in labels:
            labels[label] /= float(len(arr))
        return sum([-1*labels[index]*log(labels[index],2) for index in labels])
    else:
        raise ValueError("Attempting to calculate entropy of a non-leaf node")

def isHomogeneous(arr):
    """Returns True if all elements of array are labeled the same, else False"""
    if all(isinstance(elmnt, tuple) for elmnt in arr):
        return len(arr)==0 or all(elmnt[-1]==arr[0][-1] for elmnt in arr)
    else:
        raise ValueError("Attempting to calculate homogeneity of a non-leaf node")

def selectAttribute(arr):
    """If arr is not homogeneous, returns index of attribute with greatest information gain"""
    entropy_arr = []
    for index in xrange(len(arr[0])-1):
        sum_entropy = sum([entropy(leaf)*len(leaf)/len(arr) for leaf in split(arr, index).values()])
        entropy_arr.append((index, sum_entropy))
    best_att = min(entropy_arr, key=lambda x:x[1])
    return best_att[0] if best_att[1] < entropy(arr) else None  # check to see if no information remains

def decision_tree(tree, verbose=False):
    """Recursively perform splits to form decision tree"""
    selected_attribute = selectAttribute(tree)
    if isHomogeneous(tree) or selected_attribute is None:  # if should not be split any further
        labels = {}
        for elmnt in tree:
            if elmnt[-1] not in labels:
                labels[elmnt[-1]] = 1
            else:
                labels[elmnt[-1]] += 1
        label = max([(label,labels[label]) for label in labels], key=lambda x:x[1])[0]
        if verbose: print "\n\033[0mCurrent node is: "+str(tree)+"\n\033[94mNot splitting, label: "+label+"\033[0m"
        return label
    else:
        best_att = selected_attribute
        if verbose: print "\n\033[0mCurrent node is: "+str(tree)+"\n\033[92mSplitting on: \033[0m"+str(best_att)
        node = {}
        children = split(tree, best_att)
        for child in children:
            node[child] = decision_tree(children[child], verbose)
        return (best_att, node)

def classify(event, tree):
    if not isinstance(tree, tuple):
        print "Event "+str(event)+" has been labeled as "+tree
        return tree # reached a label
    else:
        return classify(event, tree[1][event[tree[0]]])

if __name__=="__main__":
    examples = load_csv()
    tree = decision_tree(examples)
    classify(('F', 'O'), tree)
    