
#!/usr/local/bin/python
# -*- coding: iso-8859-15 -*-


import sys
from Bio import SeqIO
from numpy import * 
from time import gmtime, strftime


class ReturnValue(object):
    def __init__(self,name,sequence):
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

def loadBlosum(file):
    handle=open(file,'r')
    blosum62=[]
    for line in handle.readlines():
        blosum62.append(map(int, line.split()))
    return blosum62
 
def globalAlignmentScore(seq1,seq2,alphabet,blosum62):
    m,n =  len(seq1)+1,len(seq2)+1    
    penalty=-4;                       
    score=zeros((m+1,n+1))         
    pointer=zeros((m+1,n+1))
    for i in range(1,m):
        for j in range(1,n):
            score_up=score[i-1][j]+penalty;
            score_down=score[i][j-1]+penalty;
            score_diagonal=score[i-1][j-1]+s(seq1[i-1],seq2[j-1],alphabet,blosum62);
            score[i][j]=max(score_up,score_down,score_diagonal);
            if score[i][j]==score_up:
                pointer[i][j]=1; #1 means trace up
            if score[i][j]==score_down:
                pointer[i][j]=2; #2 means trace left
            if score[i][j]==score_diagonal:
                pointer[i][j]=3; #3 means trace diagonal
    return pointer

def localAlignmentScore(seq1,seq2,alphabet,blosum62):
    m,n =  len(seq1)+1,len(seq2)+1    
    penalty=-4;                       
    score=zeros((m+1,n+1))         
    pointer=zeros((m+1,n+1))
    maxi=0
    maxj=0
    max_score=0
    for i in range(1,m):
        for j in range(1,n):
            score_up=score[i-1][j]+penalty;
            score_down=score[i][j-1]+penalty;
            score_diagonal=score[i-1][j-1]+s(seq1[i-1],seq2[j-1],alphabet,blosum62);
            score[i][j]=max(0,score_up,score_down,score_diagonal);
            if(score[i][j]==0):
                pointer[i][j]=0
            if score[i][j]==score_up:
                pointer[i][j]=1; #1 means trace up
            if score[i][j]==score_down:
                pointer[i][j]=2; #2 means trace left
            if score[i][j]==score_diagonal:
                pointer[i][j]=3; #3 means trace diagonal
            if score[i][j]>=max_score:
                maxi=i;
                maxj=j;
                max_score=score[i][j];
    return (pointer,maxi,maxj)

def traceback(pointer,seq1,seq2):
    i,j =  len(seq1)+1,len(seq2)+1  
    align1=""
    align2=""
    while pointer[i]!=0 and [j]!=0:
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
    align1=align1[::-1];    
    align2=align2[::-1];    
    return (align1,align2)

def tracebackLocal(pointer,seq1,seq2,maxi,maxj):
    i,j =  maxi,maxj
    align1=""
    align2=""
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
    align1=align1[::-1];    
    align2=align2[::-1];    
    return (align1,align2)

def getScore2(align1,align2,alphabet,blosum62):
    score=0
    penalty=-4
    for i in range(0,len(align1)):
        if align1[i]==align2[i]:                 
            score=score+s(align1[i],align2[i],alphabet,blosum62)
        else:
            score=score+penalty
    return score

def getScore(align1,align2,alphabet,blosum62):
    score=0
    penalty=-4
    for i in range(0,len(align1)):
        if align1[i]==align2[i]:                 
            score=score+s(align1[i],align2[i],alphabet,blosum62)
        elif align1[i]!=align2[i] and align1[i]!='-' and align2[i]!='-': 
            score=score+s(align1[i],align2[i],alphabet,blosum62)
        elif align1[i]=='-' or align2[i]=='-':
            score=score+penalty
    return score

def getWords(k,sequence):
    L = len(sequence)
    H = dict()
    for i in xrange(L - k -1): 
        temp = sequence[i:i + k]
        H[temp] = ""
    return H

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
        j = m - 1; i = k
        while j >= 0 and text[i] == pattern[j]:
            j -= 1; i -= 1
        if j == -1: return i + 1
        k += skip[ord(text[k])]
    return -1

def extendSequences(seq1,seq2,position1,position2,k):
    right1 = position1 
    right2 = position2 
    left1 = position1 
    left2 = position2 
    while ( (right1 + k <= len(seq1)) and (left1 - k > 0) and (right2 + k <= len(seq2)) and (left2 - k > 0) ):
        right1 = right1 + k
        right2 = right2 + k
        left1 = left1 - k
        left2 = left2 - k
    return (seq1[left1:right1],seq2[left2:right2])

def extendSequences2(seq1,position1,k):
    right1 = position1 + k
    left1 = position1
    while ( (right1 < len(seq1)) and (left1 > 0) ):
        right1 = right1 + 2
        left1 = left1 - 2
    return (seq1[left1:right1])
        
def searchMatches(word,query,database,A):
    matches = []
    for sequence in SeqIO.parse(database, "fasta") :
        #seq = sequence.format("fasta")
        seq = sequence.seq
        position = BoyerMooreHorspool(word,seq)
        if(position != -1):
            if((query.index(word) - position) > A):
                matches.append((position,seq))
    return matches


def searchMatches2(words,query,database,A):
    matches = dict()
    for sequence in SeqIO.parse(database, "fasta") :
        seq = sequence.seq
        for word in words:
            position = seq.find(word)
            if (position != -1):
                if((query.index(word) - position) < A):
                    if(matches.has_key(word)):
                        matches[word].append((position,seq))
                    else:
                        matches[word] = [(position,seq)]
                        
    return matches

def readFile(name):
    file = open(name, 'rU')
    return file               

#alphabet tiene keys manys y a y be son minus
def s(a,b,alphabet,blosum62):
    return blosum62[alphabet[a]-1][alphabet[b]-1]

def main(argv): 
    if( len(argv) == 3):
        alphabet = dict(A=1,R=2,N=3,D=4,C=5,Q=6,E=7,G=8,H=9,I=10,L=11,K=12,M=13,F=14,
                        P=15,S=16,T=17,W=18,Y=19,V=20,B=21,Z=22,X=23,
                        a=1,r=2,n=3,d=4,c=5,q=6,e=7,g=8,h=9,i=10,l=11,k=12,m=13,f=14,
                        p=15,s=16,t=17,w=18,y=19,v=20,b=21,z=22,x=23)
        
        sequence = readFasta(readFile(argv[0])).next()
        database = argv[1]
        blosum62 = loadBlosum(argv[2])
        k = 3
        A = 20
        words = getWords(k,sequence.sequence)
        matches = dict()
        sys.stdout.write("Starting\n")
        sys.stdout.write(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())+ "\n")
        #for word in words:
         #   match = searchMatches(word,sequence.sequence,database,A)
         #   if(len(match) > 0):
                #matches[word] = searchMatches(word,sequence.sequence,database,A)
        matches = searchMatches2(words,sequence.sequence,database,A)
        sys.stdout.write("Matches found\n")
        sys.stdout.write(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())+ "\n")    
        scoredMatches = dict()
        
#        for word,candidates in matches.items():
#            scoredMatches[word] = (0,"","")
#            for candidate in candidates:
#                extended = extendSequences(sequence.sequence,candidate[1],sequence.sequence.index(word),candidate[0],k)
#                pointer = localAlignmentScore(extended[0],extended[1],alphabet,blosum62)
#                alignments = tracebackLocal(pointer[0],extended[0],extended[1],pointer[1],pointer[2])
#                score = getScore(alignments[0],alignments[1],alphabet,blosum62)
#                if (score > scoredMatches[word][0]):
#                    scoredMatches[word] = (score,alignments[0],alignments[1])
                    
        for word,candidates in matches.items():
            for candidate in candidates:
                scoredMatches[word] = (-1000,"")
                extended = extendSequences(sequence.sequence,candidate[1],sequence.sequence.index(word),candidate[0],1)           
                score = getScore2(extended[0],extended[1],alphabet,blosum62)
                if (score > scoredMatches[word][0]):
                    scoredMatches[word] = (score,candidate[1])
                
        sys.stdout.write("Scores assigned\n")
        sys.stdout.write(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())+ "\n")
        #print the two highest scored alignments
        final = ""
        max = -1000
        for key,element in scoredMatches.iteritems():
            if(element[0] > max):
                final = element[1] 
                max = element[0]
        
        print "Score: " + str(max)
        print "Sequence :\n " + final
    else:
        sys.stderr.write("The program does not have any argument or the number of arguments is incorrect\n")
   
if __name__ == "__main__":
    main(sys.argv[1:])        
