#! /usr/bin/env python

import sys
import random
handle = open('./' + sys.argv[1])
matrix = list()
regulated = list()
regulators = list()
lines = 0
line = []
for i in handle:
    if '#' not in i:
       #lines+=1
      
       line = list(i.split('\t')[0:6])
       if line not in matrix:
          matrix.append([line[1].replace(' ',''),line[3].replace(' ',''),line[5].replace(' ','')])
       line = []
handle.close()



################## Get a list with internal nodes and output nodes ####################
for i in matrix:
    reg = i[0]
    if reg not in regulators:
       regulators.append(reg)

for i in matrix:
    regd = i[1]
    if regd not in regulators and regd not in regulated:
       regulated.append(regd)

################### Get list of interactions between nodes ############
'''
Returns a dictionary with regulators as key and a list av tuples with the regulated genes and the type of regulation
'''

links = dict()
for i in matrix:
    if i[0] in regulators:
       key = i[0]
       if key not in links:
          links[key] = [(i[1],i[2])]
       elif (i[1],i[2]) not in links[key]:
            links[key].append((i[1],i[2]))

###################### the number of directed links between internal nodes M* #######################
Mstar = 0
MstarSigns = dict()
Mout = 0
MoutSigns = dict()

for k,v in links.iteritems():
    for i in v:
        if i[0] in regulators:# and i[1] in ['+','-']:
           Mstar+=1
	   if i[1] not in MstarSigns:
              MstarSigns[i[1]] = 1
           else:
               MstarSigns[i[1]]+=1
        elif i[0] in regulated:# and i[1] in ['+','-']:
             Mout+=1
	     if i[1] not in MoutSigns:
                MoutSigns[i[1]] = 1
             else:
                 MoutSigns[i[1]]+=1    
'''
for i in matrix:
    if i[0] in regulators and i[1] in regulators:
       Mstar+=1
    elif i[0] in regulators and i[1] in regulated:
       Mout+=1
'''
################### AutoRegulatory motifs ############
automotifs = []
for k,v in links.iteritems():
    for j in v:
        if k == j[0] and (k,j[1]) not in automotifs:
           automotifs.append((k,j[1]))

###################### Find FFLs ################
'''
def findMotifs(motifs, signs):
    for k,v in links.iteritems():
        parent = k
        childOne = ''
        for j in v:
            childOne = j[0]
            if parent != j[0] and childOne in links and j[1] == signs[0]:
               for n in links[childOne]:
                   if n[0] != parent and n[0] != childOne and n[1] == signs[1]:
                      for m in v:
                          if n[0] == m[0] and m[1] == signs[2]:
                             if (parent, childOne,n[0]) not in motifs:
                     	        motifs.append((parent, childOne,n[0]))
'''
def findMotifs(motifs, signs):
    added = []
    for k,v in links.iteritems():
        parent = k
        childOne = ''
        for j in v:
            childOne = j[0]
            if parent != childOne and childOne in links and j[1] == signs[0]:
               for n in links[childOne]:
                   if n[0] != parent and n[0] != childOne and n[1] == signs[1] and n[0] not in regulated:
                      for m in v:
                          if n[0] == m[0] and m[1] == signs[2]:
                             if (parent, childOne,n[0]) not in motifs:#and n[0] not in added 
                     	        motifs.append((parent, childOne,n[0]))


def findMotifs2(motifs, signs):
    for k,v in links.iteritems():
        parent = k
        childOne = ''
        for j in v:
            childOne = j[0]
            if parent != j[0] and childOne in links and j[1] == signs[0]:
               for n in links[childOne]:
                   if n[0] != parent and n[0] != childOne and n[1] == signs[1] and n[0] in regulated:
                      for m in v:
                          if n[0] == m[0] and m[1] == signs[2]:
                             if (parent, childOne,n[0]) not in motifs:
                                 motifs.append((parent, childOne, n[0]))


def generateRandom(regulated,regulators):
    randomGraph = open('./randomRegulations','w')
    allgenes = regulated+regulators
    for i in range(3989):
        regulator = random.choice(allgenes)
        regulated = random.choice(allgenes)
        sign = random.choice(['+','-'])
        randomGraph.write(regulator + '\t' + regulator + '\t' + 'BNUM'+regulator + '\t' + regulated + '\t' + 'BNUM'+regulated + '\t' + sign + '\t'+'\n')

print                            
print "Number of internal nodes N*: ", len(regulators)
print "Number of output nodes Nout:", len(regulated)
print "Number of links between internal nodes M*:",Mstar
print "Type of links between internal nodes M*+ and M*-:",MstarSigns
print "Number of links from internal to outputnodes Mout:",Mout
print "Type of links from internal to output nodes M*+ and M*-:",MoutSigns
print "Number of autoregulatory motifs:",len(automotifs)


C1motifs = []; C2motifs = []; C3motifs = []; C4motifs = []
I1motifs = []; I2motifs=[]; I3motifs = []; I4motifs = []
C1 = ['+','+','+']; C2 = ['-','+','-']; C3 = ['+','-','-']; C4 = ['-','-','+']
I1 = ['+','-','+']; I2 = ['-','-','-']; I3 = ['+','+','-']; I4 = ['-','+','+']


'''
##### Z must not be an output node ##############
findMotifs( C1motifs , C1 )
findMotifs( C2motifs , C2 )
findMotifs( C3motifs , C3 )
findMotifs( C4motifs , C4 )
findMotifs( I1motifs , I1 )
findMotifs( I2motifs , I2 )
findMotifs( I3motifs , I3 )
findMotifs( I4motifs , I4 )

'''
##### Z must be an output node ##############
findMotifs2( C1motifs , C1 )
findMotifs2( C2motifs , C2 )
findMotifs2( C3motifs , C3 )
findMotifs2( C4motifs , C4 )
findMotifs2( I1motifs , I1 )
findMotifs2( I2motifs , I2 )
findMotifs2( I3motifs , I3 )
findMotifs2( I4motifs , I4 )



print
print "----FFL motifs----"
print "Num of C1:",len(C1motifs)#, C1motifs[0:5]
print "Num of C2:",len(C2motifs)#, C2motifs[0:5]
print "Num of C3:",len(C3motifs)#, C3motifs[0:5]
print "Num of C4:",len(C4motifs)#, C4motifs[0:5]
print "Num of I1:",len(I1motifs)#, I1motifs[0:5]
print "Num of I2:",len(I2motifs)#, I2motifs[0:5]
print "Num of I3:",len(I3motifs)#, I3motifs[0:5]
print "Num of I4:",len(I4motifs)#, I4motifs[0:5]
print

#generateRandom(regulated,regulators)

