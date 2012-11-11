'''
Created on Apr 18, 2011

@author: jose
'''

#!/usr/local/bin/python
# -*- coding: iso-8859-15 -*-

import pexpect
import os.path
import sys
from Bio import SeqIO
from numpy import * 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


global ha
global hb 

class ReturnValue(object):
    def __init__(self,accesions,file):
        self.accesions = accesions
        self.file = file


def writeFile(temp,file):
    for line in file:
        temp.write(line)
    return temp
        
def readFile(name):
    file = open(name, 'rU')
    return file

def checkFile(file): 
    if(os.path.isfile(file) == False):
        return False
    else:
        return True

def closeFile(file):
    if(file.closed != True):
        file.close()
            
def removeFile(file):  
    if(os.path.isfile(file) == True):
        os.remove(file)


def MultiScore(file,blosum62,alphabet):
    handle = readFile(file)
    totalscore = 0
    records = list(SeqIO.parse(handle, "fasta"))
    handle.close()
    visited = []
    columns = zeros(len(records[0].seq))
#    for record in records:
#        visited.append(record.id)
#        tovisits = [x for x in records if x.id not in visited]
#        score = 0
#        for tovisit in tovisits:
#            score = score + Score(record.seq,tovisit.seq,blosum62,alphabet)
#        print score   
#        totalscore = totalscore + score

    for record in records:
        visited.append(record.id)
        tovisits = [x for x in records if x.id not in visited]
        for tovisit in tovisits:
            for i in xrange(len(tovisit)):
                columns[i] = columns[i] + s(record.seq[i],tovisit.seq[i],blosum62,alphabet)
                    
    return totalSum(columns) 

def Score(alignment1,alignment2,blosum62,alphabet):
    score = 0
    for i in xrange(len(alignment1)):
        score = score + s(alignment1[i],alignment2[i],blosum62,alphabet) 
    return score

def totalSum(score):
    total = 0
    for i in score:
        total = total + i
    return total

def loadBlosum(file):
    handle=open(file,'r')
    blosum62=[]
    for line in handle.readlines():
        blosum62.append(map(int, line.split()))
    return blosum62

def s(a,b,blosum62,alphabet):
    po = -5
    pe = -1
    global ha
    global hb
    if(a!='-' and b!='-'):
        ha=0
        hb=0
        ret = blosum62[alphabet[a]-1][alphabet[b]-1]
    elif(a=='-' and b!='-'):
        if(ha>0):
            ret = pe
        else:
            ret = po
        ha = ha+1
        hb = 0
    elif(b=='-' and a!='-'):
        if(hb>0):
            ret = pe
        else:
            ret = po
        ha = 0
        hb = hb+1
    elif(a=='-' and b=='-'):
        ret = 0
        ha=0
        hb=0
    return ret
def Plot(score1,score2):
    difference = []
    #score es un dict de dict ( total score for each multialignment for each file)
    for i in xrange(len(score1)):
        difference.append(score1[i] - score2[i])
        
    fig = plt.figure()
    fig.subplots_adjust(bottom=0.2)
    ax = fig.add_subplot(111)
    plt.scatter(difference,score2,c='b',alpha=0.7,cmap=cm.Paired)
    plt.show()
        
def main(argv): 
    if( len(argv) >= 2):
        ha = 0
        hb = 0
        myscore = []
        truescore = []
        listing = [s for s in os.listdir(argv[0])
         if os.path.isfile(os.path.join(argv[0], s))]
        listing.sort(key=lambda s: os.path.getmtime(os.path.join(argv[0], s)))

        alphabet = dict(A=1,R=2,N=3,D=4,C=5,Q=6,E=7,G=8,H=9,I=10,L=11,K=12,M=13,F=14,
                        P=15,S=16,T=17,W=18,Y=19,V=20,B=21,Z=22,X=23,
                        a=1,r=2,n=3,d=4,c=5,q=6,e=7,g=8,h=9,i=10,l=11,k=12,m=13,f=14,
                        p=15,s=16,t=17,w=18,y=19,v=20,b=21,z=22,x=23)
        
        blosum62 = loadBlosum(argv[1])
        
        for infile in listing:
            if('facit' not in infile):
                command = './muscle3.8.31_i86linux32' + ' -in ' + argv[0] + '/' + infile + ' -out' + ' fileout.fa'
                child = pexpect.spawn (command)
                child.expect(pexpect.EOF)
                myscore.append(MultiScore('fileout.fa',blosum62,alphabet))
            else:
                truescore.append(MultiScore(argv[0] + '/' + infile,blosum62,alphabet))

        Plot(myscore,truescore)
        
    else:
        sys.stderr.write("The program does not have any argument or the number of arguments is incorrect\n")

if __name__ == "__main__":
    main(sys.argv[1:])        
        