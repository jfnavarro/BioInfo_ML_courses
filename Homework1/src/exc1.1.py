#! /usr/bin/env python

import sys
#handle = open('./' + sys.argv[1])
handle = open('RegulonDB')
matrix = list()
regulated = list()
regulators = set()
automotifs = list()
internos = list()
lines = 0
Mstar = 0
MstarSigns = dict()
Mout = 0
MoutSigns = dict()
links = dict()

class Motif(object):
    def __init__(self,node1="",node2="",node3=""):
        self.node1 = node1
        self.node2 = node2
        self.node3 = node3

class Tf(object):
    def __init__(self,regulator="",regulated="",sign=""):
        self.regulator = regulator
        self.regulated = regulated
        self.sign = sign

for i in handle:
    if '#' not in i:
       lines+=1
       line = list(i.split('\t')[0:6])
       if line not in matrix:
          matrix.append(line)
          if (line[1] not in internos):
              internos.append(line[1])
          tf = Tf()
          tf.regulator = line[1]
          tf.regulated = line[3]
          tf.sign = line[5]
          if(tf not in regulators and line[5] in ["+","-"]):
              if (line[1] == line[3]):
                  automotifs.append(line[1])
              else:
                  regulators.add(tf)
          else:
              automotifs.append(line[1])
print len(regulators)
          
               
              
              
              
handle.close()
################## Get a list with output nodes ####################

def isRegulated(node):
    for aux in matrix:
        if (aux[1] == node):
            return True
    return False

for i in matrix:
    regd = i[3]
    if regd not in regulated and regd not in internos:
       regulated.append(regd)

################### Get list of interactions between nodes ############




for i in internos:
    for j in matrix:
            if(j[3] == i): # the number of directed links between internal nodes M*
                Mstar += 1
                if(j[3] in MstarSigns):
                    MstarSigns[j[5]] += 1
                else:
                    MstarSigns[j[5]] = 0      
            else:
                Mout += 1
                if(j[5] in MoutSigns):
                    MoutSigns[j[5]] += 1
                else:
                    MoutSigns[j[5]] = 0


def findRegulators(regulator1,sign):
    found = list()
    for regulator in regulators:
        if(regulator.regulated == regulator1 and regulator.sign == sign):
            found.append(regulator) #comprobar es el mismo??
    return found

def findRegulators2(regulator1,regulator2):
    found = list()
    for regulator in regulators:
        if(regulator.regulator == regulator2 and regulator.regulated == regulator1):
            found.append(regulator) #comprobar es el mismo??
    return found
    
def isThere(motifs,m):
    for mot in motifs:
        if(mot.node1 == m.node1 and mot.node2 == m.node2 and mot.node3 == m.node3 or m.node1 == m.node2 or m.node2 == m.node3 or m.node1 == m.node3):
            return True
    return False


def findMotifs(signs):
    motifs = set()
    for regulator in regulators:
        m = Motif()
        if(regulator.sign == signs[0]):
            m.node1 = regulator.regulator
            found = findRegulators(regulator.regulator,signs[1])
            if(len(found) > 0):
                for regulator2 in found:
                    m.node2 = regulator2.regulator
                    found2 = findRegulators(regulator2.regulator,signs[2])
                    if(len(found2) > 0):
                        for regulator3 in found2:
                            m.node3 = regulator3.regulator
                            found3 = findRegulators2(regulator3.regulator,regulator.regulator)
                            if(len(found3) > 0):
                                m.node3 = regulator3.regulator
                                if(isThere(motifs,m) == False):
                                    motifs.add(m)
                                    #break
                                #regulators.remove(regulator)
                       # break
    return motifs

###################### Find C1 ################
#def findMotifs(motifs, signs):
#    for k,v in links.iteritems():
#        parent = k
#        childOne = ''
#        for j in v:
#            if k != j[0] and j[1] == signs[0]: ## if k not in automotif
#               childOne = j[0]
#               if childOne in links:  ##if j[0] in regulatory
#                  for n in links[childOne]:
#                      if n[0] != parent and n[0] != childOne and n[1] == signs[1]:
#                         for m in v:
#                             if n[0] == m[0] and m[1] == signs[2]:
#                                if (parent, childOne,n[0]) not in motifs:
#                     	           motifs.append((parent, childOne,n[0]))


print                            
print "Number of internal nodes N*: ", len(internos)
print "Number of output nodes Nout:", len(regulated)

print "Number of links between internal nodes M*:",Mstar
print "Type of links between internal nodes M*+ and M*-:",MstarSigns
print "Number of links from internal to outputnodes Mout:",Mout
print "Type of links from internal to output nodes M*+ and M*-:",MoutSigns
print "Number of autoregulatory motifs:",len(automotifs)





C1 = ['+','+','+']; C2 = ['-','+','-']; C3 = ['+','-','-']; C4 = ['-','-','+']
I1 = ['+','-','+']; I2 = ['-','-','-']; I3 = ['+','+','-']; I4 = ['-','+','+']

C1motifs = findMotifs(C1 )
C2motifs = findMotifs(C2 )
C3motifs = findMotifs(C3 )
C4motifs = findMotifs(C4 )
I1motifs = findMotifs(I1 )
I2motifs = findMotifs(I2 )
I3motifs = findMotifs(I3 )
I4motifs = findMotifs(I4 )

print
print "----FFL motifs----"
print "Num of C1:",len(C1motifs)#, C1motifs
print "Num of C2:",len(C2motifs)#, C2motifs
print "Num of C3:",len(C3motifs)#, C3motifs
print "Num of C4:",len(C4motifs)#, C4motifs
print "Num of I1:",len(I1motifs)#, I1motifs
print "Num of I2:",len(I2motifs)#, I2motifs
print "Num of I3:",len(I3motifs)#, I3motifs
print "Num of I4:",len(I4motifs)#, I4motifs
print
'''
print "Output:"
print  regulated
print
print "TF:"
print regulators
print
for k,v in links.iteritems():
    print k,v
'''


