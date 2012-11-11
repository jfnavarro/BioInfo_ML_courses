#!/usr/local/bin/python
# -*- coding: iso-8859-15 -*-

import os.path
import sys
import getopt
from time import gmtime, strftime


#decorator for tail recursion
class TailRecurseException:
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs

def tail_call_optimized(g):
    def func(*args, **kwargs):
        f = sys._getframe()
        if f.f_back and f.f_back.f_back and f.f_back.f_back.f_code == f.f_code:
            raise TailRecurseException(args, kwargs)
        else:
            while 1:
                try:
                    return g(*args, **kwargs)
                except TailRecurseException, e:
                    args = e.args
                    kwargs = e.kwargs
    func.__doc__ = g.__doc__
    return func

    
class ReturnValue(object):
    def __init__(self,name="",sequence=""):
        self.sequence = sequence
        self.name = name

class ReturnValue2(object):
    def __init__(self,filtradas="",nofiltradas=""):
        self.filtradas = filtradas
        self.nofiltradas = nofiltradas
        
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


def getCandidates(length,files,man,min):
    
    sequences = [readFasta(readFile(x)).next() for x in files]
    #check if the files are empty
    sys.stdout.write("Processing sequences\n") 
    candidates = []
    TempCandidates = dict()
    Totalcandidates = []
    for sequence in sequences:
        if(len(sequence.sequence) > 40):
            #candidates = permuteSequences4(sequence.sequence,length,[x.sequence for x in sequences if x!=sequence])
            candidates = permuteSequences3(sequence.sequence,length,max,min)
            #Totalcandidates[sequence.name] = set(candidates) 
        Totalcandidates.append(ReturnValue(sequence.name,candidates))  
    
    sys.stdout.write("Searching for Primers\n") 
    for candi in Totalcandidates:
        temp = set()
        temp2 = set()
        for x in Totalcandidates:
            if x != candi:
                temp2 = temp2 | (set(x.sequence.nofiltradas))
        #temp.update(candi.sequence.filtradas.difference(set(x.sequence.nofiltradas)))
        temp = candi.sequence.filtradas - temp2
        TempCandidates[candi.name] = list(temp)
    
    return TempCandidates



@tail_call_optimized
def permuteSequences2(sequence,length,candidates):
    if(len(sequence)==0):
        return candidates
    elif(sequence[:length] not in candidates):
        candidates.append(sequence[:length])
        return permuteSequences2(sequence[length:],length,candidates)
    else:
        return permuteSequences2(sequence[length:],length,candidates)         

def permuteSequences3(sequence,length,maGcc,minGcc):
    words = set()
    wordsNoFilter = []
    L = len(sequence)
    for i in xrange(L - length-1): 
        temp = sequence[i:i + length]
        gcc = gcContent(temp)
        wordsNoFilter.append(temp)
        #if(gcc > minGcc and gcc < maGcc and len(temp) == length):
        if(gcc > minGcc and gcc < 0.60 and len(temp) == length):
            words.add(temp)
    #words = set (words)
    return ReturnValue2(words,wordsNoFilter)

def permuteSequences4(sequence,length,sequences):
    words = []
    L = len(sequence)
    for i in xrange(L-length+1):
        temp = sequence[i:i+length]
        #if(gcContent(temp) > 0.40 and gcContent(temp) < 0.60):
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

def WriteCandidates(candidates,output="output.txt"):
    fileHandle = open (output, 'w' )
    for key,value in candidates.iteritems():
        fileHandle.write("Candidates for: " + key + "\n")
        fileHandle.write(str(value))
        fileHandle.write("\n\n")
    fileHandle.close()
       
def main(argv): 

    length = 20  
    finalfile = False
    output = "output.txt"
    maGcc = 0.90
    minGcc = 0.10
    candidates = dict()
    sys.stdout.write("Starting\n")
    sys.stdout.write(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())+ "\n")
    #sys.setrecursionlimit(150000)
    try:                                
        opts, args = getopt.getopt(argv, "hma:mi:o:l:", ["help","maxgcc=","mingcc=","Ofile=","length="])  
    except getopt.GetoptError:  
        sys.stdout.write("primer <filenames> | -l <lenght> | -o <file> | -M <gccmax> | -m <gccmin>\n")
        sys.stdout.write("primer -h <to get help>\n")   
        sys.exit(2)  
            
    for opt, arg in opts:                
        if opt in ("-h", "--help"):   
            sys.stdout.write("primer <filenames> | -l <lenght> | -o <file> | -ma <gccmax> | -mi <gccmin>\n")    
            sys.exit()                 
        elif opt in ('-l', "--length"):                
            length = int(arg)
        elif opt in ('-ma', "--max"):                
            maGcc = float(arg)
        elif opt in ('-mi', "--min"):                
            minGcc = float(arg)
        elif opt in ('-o', "--file"): 
            output = arg 
            finalfile = True   
            
    files = args
    
    if( (len(files) < 2) or not(checkFiles(files)) ):
        sys.stderr.write("Error: Number of files incorrect or file name not found\n")
        sys.exit()
    if(maGcc <= minGcc or maGcc <0.50 or maGcc > 0.90 or minGcc <0.10 or minGcc >0.50):
        sys.stderr.write("Error: Values introduced for the GCC content were incorrect\n")
        sys.exit()
    else:
        candidates = getCandidates(length,files,maGcc,minGcc)
        sys.stdout.write("Finished\n")
        sys.stdout.write(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + "\n")
        for key in candidates.keys():
            sys.stdout.write("Candidates for: " + str(key) + "\n")
            sys.stdout.write(str(len(candidates[key])) + "\n")       
        if(finalfile):
            WriteCandidates(candidates,output)    
                    
if __name__ == "__main__":
    main(sys.argv[1:])      