'''
Created on Apr 18, 2011

@author: jose
'''

#!/usr/local/bin/python
# -*- coding: iso-8859-15 -*-

import os.path
import sys
from Bio import SeqIO
import scipy.optimize
from scipy import optimize
from numpy import *  


class ReturnValue(object):
    def __init__(self,accesions,file):
        self.accesions = accesions
        self.file = file

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


def getSequences(file):
    handle = readFile(file)
    records = list(SeqIO.parse(handle, "fasta"))
    handle.close()
    return records

def qprime(x):
    betha = 0.5
    return 0.25*-4*betha*scipy.exp(-4*betha*x) 

def qprime2(x):
    betha = 0.5
    alpha = 2*betha
    return 0.25*(-4*betha*scipy.exp(-4*betha*x)-2*-2*(alpha+betha)*exp(-2*(alpha+betha)*x))
def q1(x):
    betha = 0.5
    return 0.25*(1 - scipy.exp(-4*betha*x))

def q2(x):
    betha = 0.5
    alpha = 2*betha
    return 0.25*(1 - scipy.exp(-4*betha*x)-2*scipy.exp(-2*(alpha+betha)*x))

def getKimura():
    st = scipy.optimize.newton(q1, 0.5, qprime, maxiter=100)
    ut = scipy.optimize.newton(q2, 0.5, qprime, maxiter=100)
    rt = 1-2*st-ut
    matrix = dict(AA=rt,AC=st,AG=ut,AT=st,CA=st,CC=rt,CG=st,CT=ut,GA=ut,GC=st,GG=rt,GT=st,TA=st,TC=ut,
                        TG=st,TT=rt,aa=rt,ac=st,ag=ut,at=st,ca=st,cc=rt,cg=st,ct=ut,ga=ut,gc=st,gg=rt,gt=st,ta=st,tc=ut,
                        tg=st,tt=rt)
    return matrix



def viterbi(kimura,seq1,seq2,s,e,t,q):
    n = len(seq1)
    m = len(seq2)
    vm=zeros((n,m))         
    vx=zeros((n,m))
    vy=zeros((n,m)) 
    vm[0][0] = 1
    
    for i in xrange(1,n):
        for j in xrange(1,m):
            aux1 = (1-2*s-t)*vm[i-1][j-1]
            aux2 = (1-e-t)*vx[i-1][j-1]
            aux3 = (1-e-t)*vy[i-1][j-1]
            vm[i][j] = q*kimura[seq1[i]+seq2[j]]*max(aux1,aux2,aux3)
            vx[i][j] = q*max((s*vm[i-1][j]),(e*vx[i-1][j]))
            vy[i][j] = q*max((s*vm[i][j-1]),(e*vx[i][j-1]))
    maxvm = getMax(vm,n,m) 
    maxvx = getMax(vx,n,m)
    maxvy = getMax(vy,n,m)       

    ve = t*max(maxvm,maxvx,maxvy)
    
    return ve

def getMax(list,n,m):
    maxi = 0
    for i in xrange(0,n):
        for j in xrange(0,m):
            if(list[i][j]>maxi):
                maxi = list[i][j]
    return maxi

def main(argv): 
    if( len(argv) >= 1):
        if(checkFile(argv[0])):
            sequences = getSequences(argv[0])
            kimura = getKimura()
            sigma = 0.3
            epsilon = 0.1
            tetha = 0.2
            qx = 0.25
            #phylip = zeros((len(sequences),len(sequences)))
            phylip = dict()
            for sequence1 in sequences:
                for sequence2 in sequences:
                    phylip[sequence1.id + sequence2.id] = viterbi(kimura,sequence1.seq,sequence2.seq,sigma,epsilon,tetha,qx)
            
            print phylip
        
        else:
            sys.stderr.write("Error in the file\n")  
    else:
        sys.stderr.write("The program does not have any argument or the number of arguments is incorrect\n")

if __name__ == "__main__":
    main(sys.argv[1:])        
        
