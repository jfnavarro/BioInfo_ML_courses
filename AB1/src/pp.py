#This software is a free software. Thus, it is licensed under GNU General Public License.
#Python implementation to Smith-Waterman Algorithm for Homework 1 of Bioinformatics class.
#Forrest Bao, Sept. 26 <http://fsbao.net> <forrest.bao aT gmail.com>

import sys, string
from numpy import *

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
        yield  "".join(sequences)   
    infile.close()
    
    
    
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

#read the first sequence
f1=open(sys.argv[1], 'r')
seq1=readFasta(f1).next()

#read the second sequence
f2=open(sys.argv[2], 'r')
seq2=readFasta(f2).next()


m,n =  len(seq1)+1,len(seq2)+1    #length of two sequences

penalty=-4;            #define the gap penalty

#generate DP table and traceback path pointer matrix
score=zeros((m+1,n+1))         #the DP table
pointer=zeros((m+1,n+1))     #to store the traceback path

#score = [0]*m
#for i in range(n):
#    score[i] = [0] * n
#pointer = [0]*m
#for i in range(n):
#    pointer[i] = [0] * n
    
P=0;

def match_score(alpha,beta):    #the function to find match/dismatch score from BLOSUM62 by letters of AAs
    if(alpha==beta):
        return 2
    else:
        return -1

max_score=P;        #initial maximum score in DP table

#calculate DP table and mark pointers
for i in range(1,m):
    for j in range(1,n):
        score_up=score[i-1][j]+penalty;
        score_down=score[i][j-1]+penalty;
        score_diagonal=score[i-1][j-1]+match_score(seq1[i-1],seq2[j-1]);
        #score[i][j]=max(0,score_up,score_down,score_diagonal);
        score[i][j]=max(score_up,score_down,score_diagonal);
        if score[i][j]==0:
            pointer[i][j]=0; #0 means end of the path
        if score[i][j]==score_up:
            pointer[i][j]=1; #1 means trace up
        if score[i][j]==score_down:
            pointer[i][j]=2; #2 means trace left
        if score[i][j]==score_diagonal:
            pointer[i][j]=3; #3 means trace diagonal
        if score[i][j]>=max_score:
            max_i=i;
            max_j=j;
            max_score=score[i][j];
#END of DP table


align1,align2='','';    #initial sequences

i,j=max_i,max_j;    #indices of path starting point

#traceback, follow pointers
while pointer[i][j]!=0:

    if pointer[i][j]==3:
        align1=align1+seq1[i-1];
        align2=align2+seq2[j-1];
        i=i-1;
        j=j-1;
    elif pointer[i][j]==2:
        align1=align1+'-';
        align2=align2+seq2[j-1];
        j=j-1;
    elif pointer[i][j]==1:
        align1=align1+seq1[i-1];
        align2=align2+'-';
        i=i-1;
#END of traceback

align1=align1[::-1];    #reverse sequence 1
align2=align2[::-1];    #reverse sequence 2


print "Length1: " + str(len(align1)) + " Length2: " + str(len(align2))          
print align1
print align2        



