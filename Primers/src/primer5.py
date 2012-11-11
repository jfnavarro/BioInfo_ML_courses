#!/usr/local/bin/python
# -*- coding: iso-8859-15 -*-

import os.path
import sys
from time import gmtime, strftime
import getopt

#Dictionary class modified to be able to look up for keys and values
class Lookup(dict):

    def __init__(self, items=[]):
        dict.__init__(self, items)

    def get_key(self, value):
        return [item[0] for item in self.items() if item[1] == value]

    def get_value(self, key):
        return self[key]

#Object for each sequence
class ReturnValue(object):
    def __init__(self, name="", sequence=""):
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

#search algorithm                       
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

#hashea the sequence with the hash table given
def doHash(sequence,h):

    x=""
    segment = len(sequence) / 4                    
    for index in xrange(segment):
        x +=(h[sequence[index:index + 4]])
        index += 1   
    return x

#return a hash table
def getHash():
    h = {}
    c = chr(0)
    s = "ATCG"
    for i in xrange(0, 4):
        for j in xrange(0, 4):
            for k in xrange(0, 4):
                for l in xrange(0, 4):
                    hashkey = s[i:i + 1] + s[j:j + 1] + s[k:k + 1] + s[l:l + 1]
                    h[hashkey] = c
                    if(ord(c)<255):
                        c = chr(ord(c)+1)    
    return h

#reconvert a sequence to its original values given its hash table
def redoHash(csequence, hash):
    sequence = []
    hash = Lookup(hash)
    for i in csequence: 
        d = ""
        for j in i:
            d += ",".join(hash.get_key(j))
        sequence.append(d)
    return sequence


#divide a file in pars of a size given
def split_seq(seq, size):
    return [seq[i:i + size] for i in range(0, len(seq), size)]

#return a dictionary with all the candidates for a length a list of files given
def getCandidates(length, files):
    
    sequences = [readFasta(readFile(x)).next() for x in files]
    #check if the files are empty
    sys.stdout.write("Sequences processed\n") 
    #hashtable = getHash()
    TempCandidates = dict()
    Totalcandidates = []
    for sequence in sequences:
        l = len(sequence.sequence)
        size = int(l/(length))
        sequencedivided = split_seq(sequence.sequence,size)
        #add missed sequences after having been splitted
        if ((len(sequence.sequence) % size) > 0 ):
            sequencedivided[len(sequencedivided)-1] += (sequence.sequence[l - (l % size):])
        candidates = []
        #obtaion all the possible candidates for the sequence
        for sqdiv in sequencedivided:
            x = permuteSequences3(sqdiv,length)
            candidates.extend(x)
            
        candidates = set(candidates)
        
#        for x in candidates:
#            ccandidates.add(doHash(x,hashtable))

        Totalcandidates.append(ReturnValue(sequence.name,candidates))
    #compare that the primers are not locate in the other sequences
    for candi in Totalcandidates:
        temp = set()
        temp2 = set()
        for x in Totalcandidates:
            if x != candi:
                temp2 = temp2 | (set(x.sequence.nofiltradas))
        #temp.update(candi.sequence.filtradas.difference(set(x.sequence.nofiltradas)))
        temp = candi.sequence.filtradas - temp2
        TempCandidates[candi.name] = list(temp)
#        TempCandidates[candi.name] = redoHash(list(temp),hashtable)

           
    return TempCandidates    

#generate all the possible combinatiosn of genomes of longitude lenght that are unique
def permuteSequences3(sequence, length):
    words = set()
    L = len(sequence)
    if(L==20):
        gcc = gcContent(sequence)
        if(gcc > 0.40 and gcc < 0.60 ):
            words.append(sequence)
    else:
        for i in xrange(L - length-1): 
            temp = sequence[i:i + length]
            gcc = gcContent(temp)
            if(gcc > 0.40 and gcc < 0.60 and len(temp) == 20):
                words.add(temp)
    return words


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
        yield  ReturnValue(title, "".join(sequences))    
    infile.close()

def WriteCandidates(candidates):
    fileHandle = open ( 'output.txt', 'w' )
    for key,value in candidates.iteritems():
        fileHandle.write("Candidates for: " + key + "\n")
        fileHandle.write(str(value))
        fileHandle.write("\n\n")
    fileHandle.close()
    
def main(argv): 

    length = 20  
    finalfile = False
    candidates = dict()
    sys.stdout.write("Starting\n")
    sys.stdout.write(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + "\n")
    try:                                
        opts, args = getopt.getopt(argv, "hfl:", ["help", "file" "length="]) 
    except getopt.GetoptError:  
        sys.stdout.write("primer <filenames> | -l <lenght> | -f \n")
        sys.stdout.write("primer -h <to get help>")   
        sys.exit(2)  
            
    for opt, arg in opts:                
        if opt in ("-h", "--help"):   
            sys.stdout.write("Help")     
            sys.exit()                 
        elif opt in ('-l', "--length"):                
            length = arg
        elif opt in ('-o', "--file"):  
            finalfile = True
    
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
        if(finalfile):
            WriteCandidates(candidates)     
           
if __name__ == "__main__":
    main(sys.argv[1:])      