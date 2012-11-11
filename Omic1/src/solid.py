#!/usr/bin/env python

# -*- coding: iso-8859-15 -*-
'''
Created on Jan 27, 2011

@author: Jose Fernandez Navarro

'''

import sys
import os.path


colorspace = dict(A0="A",A1="C",A2="G",A3="T",
                  C1="A",C0="C",C3="G",C2="T",
                  G2="A",G3="C",G0="G",G1="T",
                  T3="A",T2="C",T1="G",T0="T",);
                              
adapter = "33020103031"   
adapter2 = "CGCCTTGGCCGT"                         

class ReturnValue(object):
    def __init__(self,name="",sequence=""):
        self.sequence = sequence
        self.name = name
        
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

def convertToLetters(sequence):
    letters = ""
    if(sequence[0] != "T"):
        return letters
    else:
        base = colorspace[sequence[0:2]]
        letters += base
        for i in sequence[2:]:
            newbase = colorspace[base+i]
            letters += newbase
            base = newbase
    return letters

def convertToLetters2(sequence):
    letters = ""
    if(sequence[0] != "T"):
        return letters
    else:
        base = colorspace[sequence[0:2]]
        letters += base
        for i in sequence[2:]:
            newbase = colorspace[base+i]
            letters += newbase
            base = newbase
    return letters
       
def readFile(name):
    file = open(name, 'rU')
    return file
   

def main(argv): 
    if( len(argv) < 1):
        sys.stderr.write("Error: Number of arguments incorrect\n")
        sys.exit()
    else:
        converted = []
        if(os.path.isfile(argv[0])):
            infile = argv[0]
            handler = readFile(infile)
            colorsequences = readFasta(handler)
            for i in colorsequences:
                if(adapter not in i.sequence):
                    temp = convertToLetters(i.sequence)
                    converted.append( ReturnValue(i.name,temp))   
                   
            print len(converted)            
            

if __name__ == "__main__":
    main(sys.argv[1:])  