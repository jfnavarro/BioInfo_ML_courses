#!/usr/local/bin/python
# -*- coding: iso-8859-15 -*-

import os.path
import sys
import getopt
from time import gmtime, strftime


"object type for the sequences"
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
            
def preprocessForBadCharacterShift(self,pattern):
    map = { }
    for i in xrange(len(pattern)-1, -1, -1):
        c = pattern[i]
        if c not in map:
            map[c] = i
    return map       
      
def getCandidates(length,files):
 
    sequences = [readFasta(readFile(x)).next() for x in files]
    #check if the files are empty
    sys.stdout.write("Sequences processed\n") 
    sys.stdout.write(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())+ "\n")
    Totalcandidates = dict()
    for sequence in sequences:
        candidates = []
        index = 0
        matches = []
        for aux in sequences:
            if aux != sequence:
                matches.append(aux.sequence)
        print len(matches[0]) + len(matches[1])
        while 1:
            if( (index + length-1) >= len(sequence.sequence) ):
                break
            else:
                temp = sequence.sequence[index:length+index]
                if (gcContent(temp) > 0.40 and gcContent(temp) < 0.60 and temp not in candidates and len(temp) == 20):
                    if(temp not in matches[0] and temp not in matches[1]):
                        candidates.append(temp)
                index +=1
       
        Totalcandidates[sequences.index(sequence)] = candidates
        print len(candidates)

    
    return Totalcandidates
  

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

    for key,value in candidates.iteritems():
        sys.stdout.write("Candidates for: " + str(key) + "\n")
        sys.stdout.write(str(len(value)) + "\n")             
 
                    
if __name__ == "__main__":
    main(sys.argv[1:])      