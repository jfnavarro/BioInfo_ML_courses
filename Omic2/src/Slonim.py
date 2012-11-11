#!/usr/bin/env python

# -*- coding: iso-8859-15 -*-
'''
Created on March 23, 2011

@author: Jose Fernandez Navarro

'''

import sys
import os.path
import math
                                               

class ReturnValue(object):
    def __init__(self,name="",sequence=""):
        self.sequence = sequence
        self.name = name

class kNN:
    def __init__(self):
        self.classes = [] #list of the possible classes
        self.xs = [] # list of the neighbors
        self.ys = [] # list of the classes that the neighbors  belong to
        self.k = None # numbers of neighbors


def weight(g,c):
    return 1

def distance(x,y):
    if len(x) != len(y):
        raise ValueError, "vectors must be same length"
    sum = 0
    for i in range(len(x)):
        sum += (x[i]-y[i])**2
    return math.sqrt(sum)


def neighbor(k,m,n,c):
    
    
def readFile(name):
    file = open(name, 'rU')
    return file



def permuteSequences(reference,length,read):
    L = len(reference)
    mutations = list()
    if(length > 25):
        for i in xrange(L - length-1): 

    return mutations

def missmatches(sequence1,sequence2):
    number = 0
    for i in xrange(len(sequence1)):
        if(sequence1[i] != sequence2[i]):
            number += 1
    return number

def main(argv): 
    if( len(argv) < 2):
        sys.stderr.write("Error: Number of arguments incorrect\n")
        sys.exit()
    else:
        if(os.path.isfile(argv[0]) and os.path.isfile(argv[1])):

            

if __name__ == "__main__":
    main(sys.argv[1:])  

