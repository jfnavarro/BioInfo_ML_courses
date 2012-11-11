#!/usr/local/bin/python

import os.path
import sys
        
def readFile(name):
    if ( os.path.isfile(name) == False):
        print "The file does not exist";
    else:
        file = open(name, 'r')
        return file

def closeFile(name):
    if(not file.closed):
        name.close()
    
def gcContent(genome):
    g = c = a = t = 0
    for linea in genome:
        g += linea.count("G")
        c += linea.count("C")
        a += linea.count("A")
        t += linea.count("T")
    return float(g+c)/float(a+t+g+c)


def main(argv): 
    if( len(argv) > 0):
        for arg in argv:
            fileName = readFile(arg)
            print '%.2f'%(gcContent(fileName))
            closeFile(fileName)
    else:
        print "The program does not have any argument" 

if __name__ == "__main__":
    main(sys.argv[1:])

        