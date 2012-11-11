#!/usr/bin/env python

# -*- coding: iso-8859-15 -*-


import sys
import os.path
from numpy import *                                                    

class ReturnValue2(object):
    def __init__(self,score,pointer,maxi,maxj,max):
        self.score = score
        self.pointer = pointer
        self.maxi = maxi
        self.maxj = maxj
        self.max = max

class ReturnValue(object):
    def __init__(self,name="",sequence=""):
        self.sequence = sequence
        self.name = name

class Combination(object):
    def __init__(self,score,a,b,c):
        self.score = score
        self.a = a
        self.b = b
        self.c = c
class FastaRecord(object):
    def __init__(self, title, sequence):
        self.title = title
        self.sequence = sequence

def read_fasta_record(infile):

    line = infile.readline()

    #if not line.startswith(">"):
        #raise TypeError("Not a FASTA file: %r" % line)

    title = line[1:].rstrip()

    sequence_lines = []
    while 1:

        line = infile.readline().rstrip()
        if line == "":
            # Reached the end of the record or end of the file
            break
        sequence_lines.append(line)

    sequence = "".join(sequence_lines)
    
    return FastaRecord(title, sequence)


def read_fasta_records(input_file):
    records = []
    while 1:
        record = read_fasta_record(input_file)
        if record is None:
            break
        records.append(record)
    return records

def readFile(name):
    file = open(name, 'rU')
    return file


def overlapmatches(seq1,seq2,score,d,pointer):
    maxtotal = 0
       
    d = -4   #gap penalty
    n = len(seq1) +1 
    m = len(seq2) +1
            
    score=zeros((n,m))         
    pointer=zeros((n,m)) 
    
    for i in xrange(1,len(seq1)+1):
        for j in xrange(1,len(seq2)+1):
            left = score[i][j-1] + d #insertion 
            up = score[i-1][j] + d  #deletion 
            corner = score[i-1][j-1] + s(seq1[i-1],seq2[j-1]) #match
            auxmax = max(0,corner,left,up)
            score[i][j] = auxmax
            if(auxmax == up):
                pointer[i][j] = 1
            elif(auxmax == left):
                pointer[i][j] = 2
            elif(auxmax == corner):
                pointer[i][j] = 3 
            else:
                pointer[i][j] = 0    
            if score[i][j]>=maxtotal:
                maxtotal=score[i][j];
                
    return  maxtotal         



def s(a,b):
    if(a == b):
        return 2
    else:
        return -1

            
def main(argv): 
    if( len(argv) < 1):
        sys.stderr.write("Error: Number of arguments incorrect\n")
        sys.exit()
    else:
        if(os.path.isfile(argv[0])):
            infile = argv[0]
            handler = readFile(infile)
            tableScore = dict()
            L = read_fasta_records(handler)
            for seq1 in L:
                index = 10
                maxScore = 0
                position = 0
                for seq2 in L:
                    if(seq1!=seq2):
                        while index<len(seq1):
                            result1 = overlapmatches(seq1[:index],seq2[:index])
                            aux = L[seq2:1]
                            result2 = overlapmatches(seq1[index:],aux[index:])
                            if(result1 + result2 > maxScore):
                                maxScore = result1 + result2
                                position = index
                            index = index + 10
                            
                tableScore[maxScore] = (seq1,seq2,aux,position)
                                
                maximum = max(tableScore, key=tableScore.get)
                
                print "Chimera : " + maximum[0] + " a: " + maximum[1] + " b: " + maximum[2] + " i-j " + maximum[3] 

                    

if __name__ == "__main__":
    main(sys.argv[1:])  

