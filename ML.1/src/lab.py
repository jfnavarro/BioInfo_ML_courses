'''
Created on Sep 11, 2011

@author: jose
'''

import monkdata as m
import drawtree as draw
import dtree as tree
import sys
import os.path
import random

def partition(data, fraction):
    ldata = list(data)
    random.shuffle(ldata)
    breakPoint = int(len(ldata) * fraction)
    return ldata[:breakPoint], ldata[breakPoint:]


def main(argv): 
    
    print "Entropy Monk1: " + str(tree.entropy(m.monk1))
    print "Entropy Monk2: " + str(tree.entropy(m.monk2))
    print "Entropy Monk3: " + str(tree.entropy(m.monk3))
    
    print "Average Gain Monk1(a1): " + str(tree.averageGain(m.monk1, m.attributes[0])) 
    print "Average Gain Monk1(a2): " + str(tree.averageGain(m.monk1, m.attributes[1]))
    print "Average Gain Monk1(a3): " + str(tree.averageGain(m.monk1, m.attributes[2]))
    print "Average Gain Monk1(a4): " + str(tree.averageGain(m.monk1, m.attributes[3]))
    print "Average Gain Monk1(a5): " + str(tree.averageGain(m.monk1, m.attributes[4]))
    print "Average Gain Monk1(a6): " + str(tree.averageGain(m.monk1, m.attributes[5]))
    
    print "Average Gain Monk2(a1): " + str(tree.averageGain(m.monk2, m.attributes[0])) 
    print "Average Gain Monk2(a2): " + str(tree.averageGain(m.monk2, m.attributes[1]))
    print "Average Gain Monk2(a3): " + str(tree.averageGain(m.monk2, m.attributes[2]))
    print "Average Gain Monk2(a4): " + str(tree.averageGain(m.monk2, m.attributes[3]))
    print "Average Gain Monk2(a5): " + str(tree.averageGain(m.monk2, m.attributes[4]))
    print "Average Gain Monk2(a6): " + str(tree.averageGain(m.monk2, m.attributes[5]))
    
    print "Average Gain Monk3(a1): " + str(tree.averageGain(m.monk3, m.attributes[0])) 
    print "Average Gain Monk3(a2): " + str(tree.averageGain(m.monk3, m.attributes[1]))
    print "Average Gain Monk3(a3): " + str(tree.averageGain(m.monk3, m.attributes[2]))
    print "Average Gain Monk3(a4): " + str(tree.averageGain(m.monk3, m.attributes[3]))
    print "Average Gain Monk3(a5): " + str(tree.averageGain(m.monk3, m.attributes[4]))
    print "Average Gain Monk3(a6): " + str(tree.averageGain(m.monk3, m.attributes[5]))
    
    #print "Average Gain Level 2 Monk1(a1): " + str(tree.averageGain(tree.select(m.monk1, m.attributes[0], value), m.attributes[0])) 
    #draw.drawTree(tree.buildTree(m.monk1, m.attributes, 2))

    t=tree.buildTree(m.monk1,m.attributes);
    print(tree.check(t, m.monk1test))
    print(tree.check(t, m.monk1))
    
    t2=tree.buildTree(m.monk2,m.attributes);
    print(tree.check(t2, m.monk2test))
    print(tree.check(t2, m.monk2))
    
    t3=tree.buildTree(m.monk3,m.attributes);
    print(tree.check(t3, m.monk3test))
    print(tree.check(t3, m.monk3))

if __name__ == "__main__":
    main(sys.argv[1:])  

        