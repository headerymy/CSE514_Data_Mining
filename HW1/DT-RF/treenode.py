# -*-coding:utf-8-*-

class TreeNode:
    '''
    tree node
    '''
    def __init__(self, parentnode = None):
        self.parentnode = parentnode#parent node
        self.label = None#
        self.splitattrname = None#cutting attribute
        self.children = {}#children node
        self.splitattrindex = None

    '''
    set label
    '''
    def setlabel(self, label):
        self.label = label

    '''
    set split attribute
    '''
    def setsplitattr(self, name):
        self.splitattrname = name

    '''
    set split attribute index
    '''
    def setsplistattrindex(self, index):
        self.splitattrindex = index

