#!/usr/bin/env python

# -*- coding: iso-8859-15 -*-


import sys
import os.path
from numpy import *                                                    

class ReturnValue3(object):
    def __init__(self,score,pointer):
        self.score = score
        self.pointer = pointer

class ReturnValue(object):
    def __init__(self,name="",sequence=""):
        self.sequence = sequence
        self.name = name
        
class ReturnValue2(object):
    def __init__(self,alignment1,alignment2):
        self.alignment1 = alignment1
        self.alignment2 = alignment2
          
def readFasta(infile):
    saved = None
    while 1:
        if saved is not None:
            line = saved
            saved = None
        else:
            line = infile.readline()
            if not line:
                return
        if line.isspace():
            continue
        if not line.startswith(">"):
            raise TypeError(
                "The title line must start with a '>': %r" % line)    
        title = line.rstrip()
        sequences = []
        while 1:
            line = infile.readline()
            if not line or line.isspace():
                break
            if line.startswith(">"):
                saved = line
                break
            sequences.append(line.rstrip("\n"))                    
        yield  ReturnValue(title,"".join(sequences))    
    infile.close()


def readFile(name):
    file = open(name, 'rU')
    return file


def overlapmatches(seq1,seq2,score,d,pointer):
    
    for i in xrange(1,len(seq1)+1):
        for j in xrange(1,len(seq2)+1):
            left = score[i][j-1] + d #insertion 
            up = score[i-1][j] + d  #deletion 
            corner = score[i-1][j-1] + s(seq1[i-1],seq2[j-1]) #match
            auxmax = max(corner,left,up)
            score[i][j] = auxmax
            if(auxmax == up):
                pointer[i][j] = 1
            elif(auxmax == left):
                pointer[i][j] = 2
            else:
                pointer[i][j] = 3        
    
    return ReturnValue3(score,pointer)           

def traceback(pointer,position,sequence1,sequence2):
    i = position[0] 
    j = position[1] 
    alignment1 = ""
    alignment2 = ""
    alignment3 = ""
    alignment4 = ""

    for x in xrange(position[1]-1,0,-1):
        alignment1 = sequence1[x-1] + alignment1 
        alignment2 =  '-' + alignment2 
        
    while j != 0 and i != 0:
        if (pointer[i][j] == 3):
            alignment3 = alignment3 + sequence1[i-1] 
            alignment4 = alignment4 + sequence2[j-1]
            i=i-1
            j=j-1 
        elif (pointer[i][j] == 2):
            alignment3 =  alignment3 + '-'  
            alignment4 = alignment4 + sequence2[j-1]
            j=j-1
        elif (pointer[i][j] == 1):
            alignment3 =  alignment3 + sequence1[i-1] 
            alignment4 = alignment4 + '-'
            i=i-1

    print "Length1: " + str(len(alignment3)) + " Length2: " + str(len(alignment4))
    
    alignment3 = alignment3[::-1]
    alignment1 = alignment1 + alignment3
    alignment4 = alignment4[::-1]
    alignment2 = alignment2 + alignment4
    alignment4 = ""
    for y in xrange(len(sequence2),position[1],-1):
        alignment1 =  alignment1 + '-'  
        alignment4 = sequence2[y-1] + alignment4 
    
    alignment2 = alignment2 + alignment4

    if (i >0):
        print("Non homologous beginning")
    if (j>0):
        print("Non homologous ending")
        
    print str(alignment2)  + "\n\n"
    print str(alignment1) 
      
            
    return ReturnValue2(alignment1,alignment2)


def s(a,b):
    if(a == b):
        return 1
    else:
        return -1

def getFmax(score,m,n):
    Fmax = 0
    position = (0,0)
    m = m -1
    n = n -1 
    for i in xrange(1,n):
        if(score[i][m] > Fmax):
            Fmax = score[i][m]    
            position = (i,m)
    for j in xrange(1,m):
        if(score[n][j] > Fmax):
            Fmax = score[n][j]
            position = (n,j)
    return position

def printScore(score,n,m):
    for i in xrange(n):
        for j in xrange(m):
            sys.stdout.write(str(score[i][j]) + " ")
        sys.stdout.write("\n")
            
def main(argv): 
    if( len(argv) < 2):
        sys.stderr.write("Error: Number of arguments incorrect\n")
        sys.exit()
    else:
        if(os.path.isfile(argv[0]) and os.path.isfile(argv[1])):
            infile = argv[0]
            handler = readFile(infile)
            sequence1 = readFasta(handler).next()
            infile = argv[1]
            handler = readFile(infile)
            sequence2 = readFasta(handler).next()

            d = -4   #gap penalty
            n = len(sequence1.sequence) +1 
            m = len(sequence2.sequence) +1
            
            score=zeros((n,m))         
            pointer=zeros((n,m)) 
                
            result = overlapmatches(sequence1.sequence,sequence2.sequence,score,d,pointer)
            maxposition = getFmax(result.score,m,n)
            alignment = traceback(result.pointer,maxposition,sequence1.sequence,sequence2.sequence)
                     
            
            
            #printScore(score,n,m)

if __name__ == "__main__":
    main(sys.argv[1:])  
