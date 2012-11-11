#!/usr/bin/env python

# -*- coding: iso-8859-15 -*-
'''
Created on Jan 27, 2011

@author: Jose Fernandez Navarro

'''

import sys
import os.path
                                                     

class ReturnValue(object):
    def __init__(self,name="",sequence=""):
        self.sequence = sequence
        self.name = name

class Mutation(object): 
    def __init__(self,position=0,amount=0):
        self.position = position
        self.amount = amount
          
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
##Continue searching after finding the first match??
##Create a score function to assign score to the hits
##return a list of positions and mutations
##hash the genome to an ASSCCI number 4 genes = 1 letter
##use maq approach divide the reads and put them in different dictionaries (usually the first 28bp)
##hash the reads to 24 bits integer(put the identifier in a list, similar reads same position in memory)
# hash the reference and look up for hits using the scores, itere the reference in both directions
#take a part if the same size of the template and hash it to look up in the reads
def BoyerMooreHorspool(pattern, text):
    m = len(pattern)
    n = len(text)
    if m > n: return -1
    skip = []
    
    for k in range(256): skip.append(m)
    for k in range(m - 1): skip[ord(pattern[k])] = m - k - 1
    skip = tuple(skip)
    k = m - 1
    while k < n:
        missmatched = 0
        j = m - 1; i = k
        while j >= 0 and missmatched <= 6:
            if(text[i] != pattern[j]):
                missmatched += 1
            j -= 1; i -= 1
        if j == -1: return Mutation(i + 1,missmatched)
        k += skip[ord(text[k])]
    return Mutation(-1,0)

def permuteSequences(reference,length,read):
    L = len(reference)
    mutations = list()
    if(length > 25):
        for i in xrange(L - length-1): 
            temp = reference[i:i + length]
            x = missmatches(temp,read)
            if(x <= 6 and x > 0):
                mutations.append(Mutation(i,x))
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
            infile = argv[0]
            handler = readFile(infile)
            reads = readFasta(handler)
            infile = argv[1]
            handler = readFile(infile)
            reference = readFasta(handler).next()
            readDict = dict()
            for read in reads:
                if(len(read.sequence) > 20):
                    temp = BoyerMooreHorspool(read.sequence,reference.sequence)
                    if(temp.position != -1 and temp.amount > 0):
                        readDict[read.sequence] = temp
                        #print "Sequence: " + read.sequence + " Position: " + str(temp.position) + " Amount: " + str(temp.amount)
            print len(readDict)

#            for read in reads:
#                temp = permuteSequences(reference.sequence,len(read.sequence),read.sequence)
#                if(len(temp) > 0):
#                    readDict[read.sequence] = temp
#                    #print "Sequence: " + read.sequence + " Position: " + str(temp[0].position) + " Amount: " + str(temp[0].amount)
#            print len(readDict)
            

if __name__ == "__main__":
    main(sys.argv[1:])  
