'''
Created on Apr 18, 2011

@author: jose
'''

#!/usr/local/bin/python
# -*- coding: iso-8859-15 -*-

import os.path
import sys
from Bio import SeqIO
from Bio import Phylo
import dendropy
import scipy.optimize
from scipy import optimize
from numpy import * 
import math

class CNode:  
    def __init__(self,left,right, name, leaf):
        self.left = left
        self.right = right
        self.name = name
        self.leaf = leaf


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

def getKimura():
    a = 1
    t = 1
    B = 0.5
    st = 0.25*(1 - scipy.exp(-4*B*t))
    ut = 0.25*(1 + scipy.exp(-4*B*t)-2*scipy.exp(-2*(a+B)*t))
    rt = 1-2*st-ut
    matrix = dict(AA=rt,AC=st,AG=ut,AT=st,CA=st,CC=rt,CG=st,CT=ut,GA=ut,GC=st,GG=rt,GT=st,TA=st,TC=ut,
                        TG=st,TT=rt,aa=rt,ac=st,ag=ut,at=st,ca=st,cc=rt,cg=st,ct=ut,ga=ut,gc=st,gg=rt,gt=st,ta=st,tc=ut,
                        tg=st,tt=rt)
    return matrix

def likelihood(sequences,tree):
    k = 2*len(sequences)-1
    value = 0
    kimura = getKimura()
    alphabet = ['A','C','G','T']
    for u in xrange(0,len(sequences[0])):
        for a in alphabet:
            value = value + felsenstein(tree,a,u,kimura,sequences,0,0)
    return math.log(value)
    
def getSequence(sequences,name,u):
    for seq in sequences:
        if(seq.id == name):
            return seq.seq[u]
             
def felsenstein(tree,a,u,kimura,sequences,L2,R2):
    if(tree.leaf):
        x = getSequence(sequences,tree.name,u)
        #if( x == 'A'):
         #   return [1,0,0,0]
        #elif(x == 'C'):
         #   return [0,1,0,0]
        #elif(x == 'G'):
         #   return [0,0,1,0]
        #elif(x == 'T'):
         #   return [0,0,0,1]
        if (x == a):
            return 1
        else:
            return 0
        
    else:
       
        left = tree.left
        right = tree.right
        
        for b in ['A','C','G','T']:
            L2 = L2 + kimura[a+b] * felsenstein(left,b,u,kimura,sequences,L2,R2)
            R2 = R2 + kimura[a+b] * felsenstein(right,b,u,kimura,sequences,L2,R2)
        return L2*R2
     
def main(argv): 
    if( len(argv) >= 2):
        if(checkFile(argv[0]) and checkFile(argv[1])):
            tree2 = dendropy.Tree.get_from_path(argv[1], schema="newick")
            sequences = getSequences(argv[0])
            tree2.print_plot()
            
            nodes = tree2.leaf_nodes()
                
            S1 = CNode(None,None,nodes[0].get_node_str(),True)
            S2 = CNode(None,None,nodes[1].get_node_str(),True)
            S3 = CNode(None,None,nodes[2].get_node_str(),True)
            S4 = CNode(None,None,nodes[3].get_node_str(),True)
            
            I1 = CNode(S1,S2,"I1",False)
            I2 = CNode(S3,S4,"I1",False)
  
            tree = CNode(I1,I2,"Root",False)

            print likelihood(sequences,tree)

                
            
        
    else:
        sys.stderr.write("The program does not have any argument or the number of arguments is incorrect\n")

if __name__ == "__main__":
    main(sys.argv[1:])        
        
