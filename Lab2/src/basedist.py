#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-


import os.path
import sys
import math

class gcc(object):
        
        def __init__(self, name,ratios):
            self.name = name
            self.ratios = ratios
            
        def setRatios(self,g,t,a,c):
            self.ratios = dict(ratioG=g,ratioT=t,ratioA=a,ratioC=c)
        
        def getRatios(self):
            return self.ratios
        
        def setName(self,name):
            self.name = name
        
        def getName(self):
            return self.name

def readFile(name):
    file = open(name, 'r')
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
        
def extractName(genome):
    return ""

def getRatio(genome):
    g = c = a = t = 0
    for linea in genome:
        if(linea.find(">") == -1):
            g += linea.count("G")
            c += linea.count("C")
            a += linea.count("A")
            t += linea.count("T")

    gratio = g / float((g+c+a+t))
    cratio = c / float((g+c+a+t))
    aratio = a / float((g+c+a+t))
    tratio = t / float((g+c+a+t))
    
    ratio = dict(ratioG=gratio,ratioT=cratio,ratioA=aratio,ratioC=tratio)
    
    return ratio
    
def diff(gen1Ratios,gen2Ratios):
    
    if(gen1Ratios == gen2Ratios):
        return 0
    else:
        for type, value in gen1Ratios.iteritems():
            if (type == "ratioG"):
                gratio = value  
            elif (type == "ratioC"):
                cratio = value 
            elif (type == "ratioA"):
                aratio = value 
            elif (type == "ratioT"):
                tratio = value   
        for type, value in gen2Ratios.iteritems():
            if (type == "ratioG"):
                gratio2 = value  
            elif (type == "ratioC"):
                cratio2 = value 
            elif (type == "ratioA"):
                aratio2 = value 
            elif (type == "ratioT"):
                tratio2 = value   
            
        diff = pow((aratio - aratio2),2) + pow((cratio - cratio2),2) + pow((gratio - gratio2),2) + pow((tratio - tratio2),2) 
        return round(math.sqrt(float(diff/4)),2)


def main(argv): 
    if( len(argv) > 1):
        if(checkFiles(argv) != False):
            visited = []      
            sys.stdout.write("  " + str(len(argv)) + "\n")    
            for arg in argv:
                name = arg[0:arg.find(".")]
                file = readFile(arg)
                genome = gcc(name,getRatio(file))
                visited.append(genome)
                spaces = 10 - len(genome.getName()) 
                row = genome.getName() + " "*spaces
                file.close()
                for arg2 in visited:
                    row += "   " + str(diff(genome.getRatios(),arg2.getRatios()))
                row += "\n"
                sys.stdout.write(row)
        else:
            sys.stderr.write("Some of the files are missed\n")
    else:
        sys.stderr.write("The program does not have any argument or the number of arguments is incorrect\n")

if __name__ == "__main__":
    main(sys.argv[1:])