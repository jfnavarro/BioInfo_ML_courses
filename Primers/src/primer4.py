#!/usr/local/bin/python
# -*- coding: iso-8859-15 -*-

import os.path
import sys
from time import gmtime, strftime
import getopt

class ReturnValue(object):
    def __init__(self, name="", sequence=""):
        self.sequence = sequence
        self.name = name

class ReturnValueHash(object):
    def __init__(self, hash="", csequence="", name=""):
        self.csequence = csequence
        self.hash = hash
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
    if m > n: return - 1
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
    return - 1
def doHash(sequence, name):

    h = {}
    c = 0
    s = "ATCG"
    cseq = []
    segment = len(sequence) / 4
    for i in xrange(0, 4):
        for j in xrange(0, 4):
            for k in xrange(0, 4):
                for l in xrange(0, 4):
                    hashkey = s[i:i + 1] + s[j:j + 1] + s[k:k + 1] + s[l:l + 1]
                    h[hashkey] = c
                    c += 1
    for index in xrange(segment):
        cseq.append(h[sequence[index:index + 4]])
        index += 1

    cseq.append(sequence[len(cseq) - (len(cseq) % 4)])

    return ReturnValueHash(h, cseq, name)
    
def redoHash(csequence, hash):
    sequence = []
    for i in csequence: 
        temp = ""
        for j in i:
            temp += str(find_key(hash,j))[2:6]
        sequence.append(temp)
    return sequence
#
def find_key(dic, val):
    return [k for k, v in dic.iteritems() if v == val]
  
def compareGenomes(genome1, genome2):
    matches = []
    if(genome1 != genome2):
        for i in genome1:
            if(BoyerMooreHorspool(i, genome2) == -1):
                matches.append(i)
    return matches

def compareGenomes2(genome1, genome2):
    matches = []
    if(genome1 != genome2):
        for i in genome1:
            try:
                genome2.index(i)
            except ValueError:
            #if (i not in genome2):
                matches.append(i)
    return matches

def split_seq(seq, size):
    """ Split up seq in pieces of size """
    return [seq[i:i + size] for i in range(0, len(seq), size)]
        
def getCandidates(length, files):
    
    sequences = [readFasta(readFile(x)).next() for x in files]
    #check if the files are empty
    sys.stdout.write("Sequences processed\n") 
    Totalcandidates = dict()
    tempCandidates = []
    #compressed = ([doHash(sequence.sequence, sequence.name) for sequence in sequences])
    ccandidates = []
    for csequence in sequences:
        ccandidates = permuteSequences3(csequence.sequence, length)
        print len(ccandidates)
        tempCandidates.append(ReturnValue(csequence.name, ccandidates))
    for temp in tempCandidates:
        ccandidates.append([compareGenomes2(temp.sequence, x.sequence) for x in tempCandidates])  
        print len(ccandidates)
        #Totalcandidates[temp.name] = redoHash(ccandidates, csequence.hash)
        Totalcandidates[temp.name] = ccandidates
    
    return Totalcandidates          

def permuteSequences3(sequence, length):
    words = []
    L = len(sequence)
    for i in xrange(L - length -1): 
        temp = sequence[i:i + length]
        if(gcContent(temp) > 0.40 and gcContent(temp) < 0.60):
            words.append(temp)
    words = set (words)
    return list(words)

def gcContent(sequence):
    g = c = a = t = 0
    
    g += sequence.count("G")
    c += sequence.count("C")
    a += sequence.count("A")
    t += sequence.count("T")
    
    return float(g+c)/float(a+t+g+c)
def permuteSequences4(sequence, length, sequences):
    words = []
    L = len(sequence)
    for i in xrange(L - length + 1):
        temp = sequence[i:i + length]
        #if(gcContent(temp) > 0.40 and gcContent(temp) < 0.60):
            #if(BoyerMooreHorspool(temp,sequences) == -1): 
        try:
            sequences.index(temp)
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
        yield  ReturnValue(title, "".join(sequences))    
    infile.close()

    
def main(argv): 

    length = 20  
    candidates = dict()
    sys.stdout.write("Starting\n")
    sys.stdout.write(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + "\n")
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
    if((len(files) < 2) or not(checkFiles(files))):
        sys.stderr.write("Error: Number of files incorrect or file name not found\n")
    else:
        candidates = getCandidates(length, files)
        sys.stdout.write("Finished\n")
        sys.stdout.write(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + "\n")
        for key in candidates.keys():
            sys.stdout.write("Candidates for: " + str(key) + "\n")
            sys.stdout.write(str(len(candidates[key])) + "\n")        
           
if __name__ == "__main__":
    main(sys.argv[1:])      