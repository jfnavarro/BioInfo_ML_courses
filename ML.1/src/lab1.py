'''
Created on Sep 19, 2011

@author: jfn
'''

import drawtree as draw
import dtree as tree
import monkdata as m
import random as r
from pylab import *

def partition(data, fraction):
    ldata = list(data)
    r.shuffle(ldata)
    breakPoint = int(len(ldata) * fraction)
    return ldata[:breakPoint], ldata[breakPoint:]

def getClasification(dataset,fraction):
    monk1train, monk1val = partition(dataset,fraction)
    testTree = tree.buildTree(monk1val,m.attributes)
    prunedTrees = tree.allPruned(testTree)
    pValue = 0
    for pruned in prunedTrees:
        if(tree.check(pruned,monk1train) > pValue):
            bestTree = pruned
            pValue = tree.check(pruned,monk1train)
    return pValue, bestTree

print "Entropy Monk1: " + str(tree.entropy(m.monk1))
print "Entropy Monk2: " + str(tree.entropy(m.monk2))
print "Entropy Monk3: " + str(tree.entropy(m.monk3))

print "Gain Monk1 a1: " + str(tree.averageGain(m.monk1,m.attributes[0]))
print "Gain Monk1 a2: " + str(tree.averageGain(m.monk1,m.attributes[1]))
print "Gain Monk1 a3: " + str(tree.averageGain(m.monk1,m.attributes[2]))
print "Gain Monk1 a4: " + str(tree.averageGain(m.monk1,m.attributes[3]))
print "Gain Monk1 a5: " + str(tree.averageGain(m.monk1,m.attributes[4]))
print "Gain Monk1 a6: " + str(tree.averageGain(m.monk1,m.attributes[5]))

print "Gain Monk2 a1: " + str(tree.averageGain(m.monk2,m.attributes[0]))
print "Gain Monk2 a2: " + str(tree.averageGain(m.monk2,m.attributes[1]))
print "Gain Monk2 a3: " + str(tree.averageGain(m.monk2,m.attributes[2]))
print "Gain Monk2 a4: " + str(tree.averageGain(m.monk2,m.attributes[3]))
print "Gain Monk2 a5: " + str(tree.averageGain(m.monk2,m.attributes[4]))
print "Gain Monk2 a6: " + str(tree.averageGain(m.monk2,m.attributes[5]))

print "Gain Monk3 a1: " + str(tree.averageGain(m.monk3,m.attributes[0]))
print "Gain Monk3 a2: " + str(tree.averageGain(m.monk3,m.attributes[1]))
print "Gain Monk3 a3: " + str(tree.averageGain(m.monk3,m.attributes[2]))
print "Gain Monk3 a4: " + str(tree.averageGain(m.monk3,m.attributes[3]))
print "Gain Monk3 a5: " + str(tree.averageGain(m.monk3,m.attributes[4]))
print "Gain Monk3 a6: " + str(tree.averageGain(m.monk3,m.attributes[5]))

print "Gain Level1 Monk1 a1: " + str(tree.averageGain(tree.select(m.monk1, m.attributes[0], 1),m.attributes[0]))
print "Gain Level1 Monk1 a2: " + str(tree.averageGain(tree.select(m.monk1, m.attributes[1], 1),m.attributes[1]))
print "Gain Level1 Monk1 a3: " + str(tree.averageGain(tree.select(m.monk1, m.attributes[2], 1),m.attributes[2]))
print "Gain Level1 Monk1 a4: " + str(tree.averageGain(tree.select(m.monk1, m.attributes[3], 1),m.attributes[3]))
print "Gain Level1 Monk1 a5: " + str(tree.averageGain(tree.select(m.monk1, m.attributes[4], 1),m.attributes[4]))
print "Gain Level1 Monk1 a6: " + str(tree.averageGain(tree.select(m.monk1, m.attributes[5], 1),m.attributes[5]))

print "Gain Level2 Monk1 a1: " + str(tree.averageGain(tree.select(m.monk1, m.attributes[0], 2),m.attributes[0]))
print "Gain Level2 Monk1 a2: " + str(tree.averageGain(tree.select(m.monk1, m.attributes[1], 2),m.attributes[1]))
print "Gain Level2 Monk1 a3: " + str(tree.averageGain(tree.select(m.monk1, m.attributes[2], 2),m.attributes[2]))
print "Gain Level2 Monk1 a4: " + str(tree.averageGain(tree.select(m.monk1, m.attributes[3], 2),m.attributes[3]))
print "Gain Level2 Monk1 a5: " + str(tree.averageGain(tree.select(m.monk1, m.attributes[4], 2),m.attributes[4]))
print "Gain Level2 Monk1 a6: " + str(tree.averageGain(tree.select(m.monk1, m.attributes[5], 2),m.attributes[5]))

print "Gain Level3 Monk1 a1: " + str(tree.averageGain(tree.select(m.monk1, m.attributes[0], 3),m.attributes[0]))
print "Gain Level3 Monk1 a2: " + str(tree.averageGain(tree.select(m.monk1, m.attributes[1], 3),m.attributes[1]))

print "Gain Level3 Monk1 a4: " + str(tree.averageGain(tree.select(m.monk1, m.attributes[3], 3),m.attributes[3]))
print "Gain Level3 Monk1 a5: " + str(tree.averageGain(tree.select(m.monk1, m.attributes[4], 3),m.attributes[4]))

print "Most Common Level1 Monk1 a1"

print "Monk 1 Etrain : " + str(tree.check(tree.buildTree(m.monk1, m.attributes), m.monk1))
print "Monk 1 Etest  : " + str(tree.check(tree.buildTree(m.monk1, m.attributes), m.monk1test))
print "Monk 2 Etrain : " + str(tree.check(tree.buildTree(m.monk2, m.attributes), m.monk2))
print "Monk 2 Etest  : " + str(tree.check(tree.buildTree(m.monk2, m.attributes), m.monk2test))
print "Monk 3 Etrain : " + str(tree.check(tree.buildTree(m.monk3, m.attributes), m.monk3))
print "Monk 3 Etest  : " + str(tree.check(tree.buildTree(m.monk3, m.attributes), m.monk3test))


x = [0.3,0.4,0.5,0.6,0.7,0.8]
y = []
for fraction in x:
    print fraction
    value,tree = getClasification(m.monk1,fraction)
    y.append(value)

plot(x,y)
show()       
#draw.drawTree(tree.buildTree(m.monk1,m.attributes))