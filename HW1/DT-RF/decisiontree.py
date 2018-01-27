# -*-coding:utf-8 -*-
import math
from dataset import DataSet
from treenode import TreeNode
import os

'''
Loading data
filepath: the path of file
hasTitle: has tile or not
'''
def load_data(filepath, hasTitle = False):
    print('Loading data: ' + filepath)
    if not os.path.exists(filepath):
        raise IOError(filepath + ' not exists')
        return None
    if not os.path.isfile(filepath):
        raise IOError(filepath + ' no a file')
        return None
    dataset = DataSet()
    try:
        f = open(filepath, 'r')
        line = f.readline()
        while line:
            line = line.strip()
            row = line.split(',')
            if hasTitle:
                dataset.settitle(row)
                hasTitle = False
            else:
                dataset.addrow(row)
            line = f.readline()
        f.close()
    except Exception as e:
        print(e)
    return dataset


'''
the index of attributes in the dataset will be put into different rows
'''
def getsplitcountdict(dataset, index):
    count = {}
    for row in dataset.getrows():
        count[row[index]] = count.get(row[index], 0)+1
    return count

'''
vote to get the label
'''
def findmaxlabel(dataset):
    countdict = getsplitcountdict(dataset, -1)
    maxcount = 0
    maxlabel = None
    keys = sorted(countdict.keys())
    for key in keys:
        value = countdict[key]
        if value > maxcount:
            maxcount = value
            maxlabel = key
    return maxlabel

'''
compute the Entropy of labels in dataset
'''
def calentropy1(dataset):
    count = getsplitcountdict(dataset, -1)
    entropy = 0.0
    rowcount = float(dataset.getrowcount())
    for value in count.values():
        #probability
        value = value/rowcount
        entropy -= value * math.log(value, 2)
    return entropy

'''
compute the Split Entropy
'''
def calentropy2(attr, dataset):
    count = getsplitcountdict(dataset, attr)
    entropy = 0.0
    allcount = float(dataset.getrowcount())
    for key,value in count.items():
        #the probability that the value of label equals to key value
        value = value/allcount
        #the entropy when value equals to key
        entropy += value * calentropy3(attr, key, dataset)
    return entropy

'''
compute the entropy when attr value equals to key
'''
def calentropy3(attr,key,dataset):
    countdict = {}
    count_row = 0.0
    for row in dataset.getrows():
        if row[attr] != key:
            continue
        countdict[row[-1]] = countdict.get(row[-1], 0)+1
        count_row += 1
    entropy = 0.0
    for value in countdict.values():
        value = value/count_row
        entropy -= value * math.log(value, 2)
    return entropy

'''
use attr_id to cut dataset
'''
def splitdataset(dataset, attr_id):
    subdatasets = {}
    for row in dataset.getrows():
        key = row[attr_id]
        if key in subdatasets.keys():
            subdatasets[key].addrow(row)
        else:
            tdataset = DataSet()
            #set table header
            tdataset.settitle(dataset.gettitle())
            #add rows
            tdataset.addrow(row)
            subdatasets[key] = tdataset
    return subdatasets

'''
build tree
'''
def buildTree(dataset,attrs, treeNode = None,):
    if treeNode == None:
        treeNode = TreeNode()
    #determine if the cut attribute is 0
    if len(attrs)<=0:
        #raise TypeError('len(attrs)<=0')
        #if 0, find the max
        label = findmaxlabel(dataset)
        treeNode.setlabel(label)
        return treeNode

    #determine if pure value or not
    tset = set()
    sign = True
    for row in dataset.getrows():
        tset.add(row[-1])
        if len(tset) > 1:
            sign = False
            break
    if sign:
        label = (list(tset))[0]
        treeNode.setlabel(label)
        return treeNode

    #compute the gain
    max_gain = 0.0
    attr_id = None
    entropys = calentropy1(dataset)
    for attr in attrs:
        attrentropy = calentropy2(attr, dataset)
        gain = entropys - attrentropy
        if gain > max_gain:
            max_gain = gain
            attr_id = attr

    #vote to decide if no change in entropy after cut
    if attr_id == None:

        label = findmaxlabel(dataset)
        treeNode.setlabel(label)
        return treeNode

    #set node value
    treeNode.setsplistattrindex(attr_id)
    treeNode.setsplitattr(dataset.gettitle()[attr_id])
    #classify data
    subdatasets = splitdataset(dataset, attr_id)

    #release ram
    del(dataset)
    #delete the current cutting attribute
    attrs.discard(attr_id)

    #build branch, choose the biggest branch to build
    keyset = set(subdatasets.keys())
    for x in range(len(keyset)):
        max_count = 0
        rkey = None
        for key in keyset:
            value = subdatasets[key].getrowcount()
            if value > max_count:
                max_count = value
                rkey = key
        keyset.discard(rkey)
        ctreenode = TreeNode(treeNode)
        treeNode.children[rkey] = ctreenode
        buildTree(subdatasets.get(rkey), attrs, ctreenode)
    return treeNode


'''
classify the instance
'''
def classify(tree, instance):
    if (None == tree):
        raise TypeError("Error")
        return None
    if (None != tree.label):
        print(tree.label)
        return tree.label
    return classify(tree.children[instance[tree.splitattrindex]], instance)

def printresult(tree):
    if (None == tree):
        return None
    if (None != tree.label):
        return print(tree.label)
'''
test the decision tree
'''
def testTree(dataset, tree):
    if tree == None:
        print('decision is empty')
        return
    #correct number
    rcount = 0.0
    tSet = set()

    #print the last 10 result
    printresult(tree)

    for row in dataset.getrows():
        label = classify(tree, row)
        tSet.add(label)
        if label == row[-1]:
            rcount += 1
    accuray = rcount/dataset.getrowcount()
    print('correct number: {}, total: {}'.format(rcount,dataset.getrowcount()))
    return accuray

if __name__ == '__main__':
    trainingdataset = load_data('data/trainingFile.csv',hasTitle = True)
    print('reading file completed，get {} rows of data'.format(trainingdataset.getrowcount()))
    if trainingdataset == None or trainingdataset.getrowcount() <= 0:
        print('no data for training')
    else:
        print('building decision tree')
        attrs = set(range(0, len(trainingdataset.gettitle())-1))
        tree = buildTree(trainingdataset, attrs)
        print('decision tree completed!')
        testdataset = load_data('data/testFile.csv', hasTitle = True)
        print('reading file completed，get {} rows of data'.format(testdataset.getrowcount()))
        if testdataset == None or testdataset.getrowcount() <= 0:
            print('no data for testing')
        else:
            print('testing decision tree')
            accuray = testTree(testdataset,tree)
            print('accuracy is: {:.2f}%'.format(accuray * 100))
