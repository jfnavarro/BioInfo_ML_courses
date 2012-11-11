#!/usr/local/bin/python
# -*- coding: iso-8859-15 -*-

import os.path
import sys
import getopt
from time import gmtime, strftime


 
class ReturnValue(object):
    def __init__(self,name="",sequence=""):
        self.sequence = sequence
        self.name = name
        
def readFile(name):
    file = open(name, 'rU')
    return file

def checkFiles(files):
    for file in files:
        if(os.path.isfile(file) == False):
            return False
    return True

def closeFiles(names):
    for name in names:
        if(not name.closed):
            name.close()    
               

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


def getCandidates(length,files):
    
    sequences = [readFasta(readFile(x)).next() for x in files]
    #check if the files are empty
    sys.stdout.write("Sequences processed\n") 

    Totalcandidates = dict()
    for sequence in sequences:
        #print len(sequence.sequence)
        sequencedivided = split_seq(sequence.sequence,int(round(len(sequence.sequence)/length/2)))
        candidates = []
        print len(sequencedivided)
        for sqdiv in sequencedivided:
            x = permuteSequences4(sqdiv,length,[x.sequence for x in sequences if x!=sequence])
            candidates.extend(x)
            #print "File : " + str(len(candidates)) + " Processed"
        candidates = set(candidates)
        Totalcandidates[sequence.name] = list(candidates)

    
    return Totalcandidates

def compareGenomes(genome1,genome2):
    matches = []
    if(genome1 != genome2):
        for i in genome1:
            if(BoyerMooreHorspool(i,genome2) == -1):
                matches.append(i)
    return matches

def compareGenomes2(genome1,genome2):
    matches = []
    if(genome1 != genome2):
        for i in genome1:
            try:
                genome2.index(i)
            except ValueError:
                matches.append(i)
    return matches

def split_seq(seq,size):
    """ Split up seq in pieces of size """
    return [seq[i:i+size] for i in range(0, len(seq), size)]
        
            
def permuteSequences3(sequence,length):
    words = []
    L = len(sequence)
    for i in xrange(L-length+1): 
        temp = sequence[i:i+length]
        if(gcContent(temp) > 0.40 and gcContent(temp) < 0.60):
            words.append(temp)
    words = set (words)
    return list(words)

def permuteSequences4(sequence,length,sequences):
    words = []
    L = len(sequence)
    for i in xrange(L-length+1):
        temp = sequence[i:i+length]
        gcc = gcContent(temp)
        if(gcc > 0.40 and gcc < 0.60 ):
            #if(BoyerMooreHorspool(temp,sequences) == -1): 
            try:
                [x.index(temp) for x in sequences]
            except ValueError:
                words.append(temp)
    words = set (words)
    return list(words)

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


def gcContent(sequence):
    g = c = a = t = 0
    
    g += sequence.count("G")
    c += sequence.count("C")
    a += sequence.count("A")
    t += sequence.count("T")
    
    return float(g+c)/float(a+t+g+c)
    
def main(argv): 

    length = 20  
    candidates = dict()
    sys.stdout.write("Starting\n")
    sys.stdout.write(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())+ "\n")
    #sys.setrecursionlimit(150000)
    try:                                
        opts, args = getopt.getopt(argv, "hl:", ["help", "length="]) 
    except getopt.GetoptError:  
        sys.stdout.write("primer <filenames> | -l <lenght>\n")
        sys.stdout.write("primer -h <to get help>")   
        sys.exit(2)  
            
    for opt, arg in opts:                
        if opt in ("-h", "--help"):   
            sys.stdout.write("Help")     
            sys.exit()                 
        elif opt in ('-l', "--length"):                
            length = arg
    
    files = args
    if( (len(files) < 2) or not(checkFiles(files)) ):
        sys.stderr.write("Error: Number of files incorrect or file name not found\n")
    else:
        candidates = getCandidates(length,files)
        sys.stdout.write("Finished\n")
        sys.stdout.write(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + "\n")
        for key in candidates.keys():
            sys.stdout.write("Candidates for: " + str(key) + "\n")
            sys.stdout.write(str(len(candidates[key])) + "\n")        
 
                    
if __name__ == "__main__":
    main(sys.argv[1:])      