# -*-coding:utf-8 -*-
import decisiontree
import random
from dataset import DataSet

'''
cut dataset
num: number to be cut
percent: the percentage of subset
dataset: orig dataset
'''
def splitDataset(num,percent, dataset):
    #result dateset
    rdataset = []
    #the row number of orig dataset
    tnum = dataset.getrowcount()
    #the row number in target dataset
    rownum = (int)(tnum * percent)
    for i in range(num):
        #generate different rownums in an index
        iSet = set()
        while len(iSet) < rownum:
            iSet.add(random.randrange(0,tnum))
        #build new dataset
        dset = DataSet()
        #set title
        dset.settitle(dataset.gettitle())
        #according to the index in the set to add colunm
        for index in iSet:
            dset.addrow(dataset.getrows()[index])
        rdataset.append(dset)
    return rdataset

'''
cutting attribute
num: number of attribute
percent:
tLen: size of orig attribute list
'''
def splitAttrs(num, percent, tLen):
    #result list
    rattrs = []
    #number og attribute
    anum = int(tLen * percent)
    for i in range(num):
        #generate different number of anum in index
        iSet = set()
        while len(iSet) < anum:
            iSet.add(random.randrange(0, tLen))
        #add
        rattrs.append(iSet)
    return rattrs

'''
test random forest
dataset:
forset:
'''
def testTree(dataset, forest):
    if forest == None or len(forest) == 0:
        print('forest is empty')
        return
    #number of correct
    rcount = 0.0
    for row in dataset.getrows():
        cresult = {}
        #go through all the tree
        for tree in forest:
            #single tree classify
            label = decisiontree.classify(tree,row)
            #result
            cresult[label] = cresult.get(label, 0) + 1
        count = 0
        rlabel = ''
        #statistical result
        for key,value in cresult.items():
            #majority vote
            if value > count:
                count = value
                rlabel = key
        #equal or not
        if rlabel == row[-1]:
            rcount += 1
    accuray=rcount/dataset.getrowcount()
    print('correct number: {}, total: {}'.format(rcount, dataset.getrowcount()))
    return accuray

if __name__ == '__main__':

    subsetnum = 10
    percent = 0.8

    allDataSet = decisiontree.load_data('data/trainingFile.csv', hasTitle = True)
    print('load data completed，total {} rows imported'.format(allDataSet.getrowcount()))
    if allDataSet == None or allDataSet.getrowcount() <= 0:
        print('No data used to training')
    else:
        print('cutting data...')

        dataSets = splitDataset(subsetnum,percent,allDataSet)
        print('cutting data completed')
        print('cutting attribute...')

        attrSets = splitAttrs(subsetnum,percent, len(allDataSet.gettitle()))
        print('cutting attribute completed')
        forest = []
        for i in range(subsetnum):
            print('Now building {} of {} decision tree'.format(i+1, subsetnum))
            dataset = dataSets[i]
            attrs = attrSets[i]
            tree = decisiontree.buildTree(dataset,attrs)
            print('build completed!')
            forest.append(tree)

        testdataset = decisiontree.load_data('data/testFile.csv', hasTitle = True)
        print('loading data completed，total {} rows data imported'.format(testdataset.getrowcount()))
        if testdataset == None or testdataset.getrowcount() <= 0:
            print('No data to testing')
        else:
            print('Now testing decision tree')
            accuray = testTree(testdataset,forest)
            print('accuracy: {:.2f}%'.format(accuray * 100.0))

