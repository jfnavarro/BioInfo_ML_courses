#!/usr/local/bin/python
# -*- coding: iso-8859-15 -*-

import pexpect
import os.path
import sys
import random
from Bio import SeqIO
import shutil


class ReturnValue(object):
    def __init__(self,accesions,file):
        self.accesions = accesions
        self.file = file
     
def getAccesions(fastaFile,size):
    file = ""
    accesions = dict()
    
    for record in fastaFile:
        
        if(record.find(">") != -1):
            temp = removeCrapp(record)
            
            if(accesions.__contains__(temp[0:size]) == False):    
                accesions.setdefault(temp[0:size],[temp]) 
                file += temp[0:size] + "\n"   
            else:
                while( (accesions.__contains__(temp[0:size]) == True) and (size < 10)):
                    size +=1
                if((accesions.__contains__(temp[0:size]) == False) and (size < 10)): 
                    accesions.setdefault(temp[0:size],[temp]) 
                    file += temp[0:size] + "\n"
                else:
                    size = 6
                    x = random.randint(1000,9999)
                    if(accesions.__contains__(temp[0:size] + str(x)) == False):
                        accesions.setdefault(temp[0:size] + str(x),[temp])
                        file += temp[0:size] + str(x) + "\n"
                    else:    
                        return ReturnValue(-1,-1)
            
        else:
            file += record
                   
    return ReturnValue(accesions,file)

    
def removeCrapp(chain):
    if (chain.find(" ") != -1):
        return chain[0:chain.find(" ")] + chain[chain.find("\n"):len(chain)]
    else:
        return chain   

def writeFile(temp,file):
    for line in file:
        temp.write(line)
    return temp
        
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
            
def removeFiles():  
    if(os.path.isfile('infile') == True):
        os.remove('infile')
    
    if(os.path.isfile('outfile') == True):    
        os.remove('outfile')
        
    if(os.path.isfile('intree') == True):
        os.remove('intree')
    
    if(os.path.isfile('outtree') == True):
        os.remove('outtree')
        
def main(argv): 
    if( len(argv) != 1):
        if(checkFile(argv[0]) != False): 
            if( (argv[1] > 0)):
                temp = readFile(argv[0])
                tempAccesions = getAccesions(temp,5)
                if(tempAccesions.accesions != -1):
                    temp.close()
                    #comprobar si existe infile y outfile y eliminar
                    removeFiles()
                    
                    #tempFile = tempfile.NamedTemporaryFile()
                    #input_handle = tempfile.NamedTemporaryFile()
                    input_handle = open("fasta.fa", "w")
                    input_handle.write(str(tempAccesions.file) + "\n")
                    input_handle.close()

                    output_handle = open("phylip.phy", "w")
                    input_handle = open("fasta.fa", "rU")
                    sequences = SeqIO.parse(input_handle, "fasta")
                    SeqIO.write(sequences, output_handle, "phylip")

                    input_handle.close()
                    output_handle.close()
                    
                    sys.stdout.write("Bootstraps starting\n")
                    child = pexpect.spawn ('phylip seqboot')
                    child.expect ('Please enter a new file name>')
                    child.sendline (output_handle.name)
                    sys.stdout.write("File processed\n")
                    child.sendline ('R')
                    child.sendline (argv[1])
                    sys.stdout.write("Number of Replications processed\n")
                    child.sendline ('Y')
                    child.sendline ("1")
                    sys.stdout.write("Processing data\n")
                    #child.interact()
                    child.expect(pexpect.EOF)
                    sys.stdout.write("Bootstraps generated\n")
                    
                    
                    #checkear todo bieh
                    if(os.path.isfile('outfile') == True):  
                        shutil.copy('outfile', 'infile')
                        os.remove('outfile')
                        
                        sys.stdout.write("Starting to generate Matrix of distances\n")
                        child = pexpect.spawn ('phylip protdist')
                        sys.stdout.write("File processed\n")
                        child.sendline ('M')
                        child.sendline ('D')
                        child.sendline(argv[1])
                        child.sendline ('Y')
                        sys.stdout.write("Processing data\n")
                        #child.interact()
                        child.expect(pexpect.EOF)
                        sys.stdout.write("Matrix generated\n")
                        
                        os.remove('infile')
                        if(os.path.isfile('outfile') == True):  
                            shutil.copy('outfile', 'infile')
                            os.remove('outfile')
                            
                            sys.stdout.write("Starting to generate The Neighbor Tree\n")
                            child = pexpect.spawn ('phylip neighbor')
                            sys.stdout.write("File processed\n")
                            child.sendline ('M')
                            child.sendline (argv[1])
                            child.sendline ('1')
                            child.sendline ('Y')
                            sys.stdout.write("Processing data\n")
                            #child.interact()
                            child.expect(pexpect.EOF)
                            sys.stdout.write("Tree generated\n")
                            
                            os.remove('outfile')
                            os.remove('infile')
                            if(os.path.isfile('outtree') == True):
                                tree = open('outtree','r')
                                for line in tree:
                                    sys.stdout.write(line)
                                tree.close()
                                os.remove('outtree')
                            else:
                                sys.stderr.write("There was an error processing the Tree\n")
                        else:
                            sys.stderr.write("There was an error processing the Matrix of distances\n")
                        
                    else:
                        sys.stderr.write("There was an error processing the bootstraps\n")
                    
                    #delete files
                    os.remove(input_handle.name)
                    os.remove(output_handle.name)
                    
                    
                else:
                    sys.stderr.write("There was an unexpected error decoding the accesions\n") 
            else:
                sys.stderr.write("The number of replicates is incorrect\n")   
        else:
            sys.stderr.write("The file does not exists\n")
    else:
        sys.stderr.write("The program does not have any argument or the number of arguments is incorrect\n")

if __name__ == "__main__":
    main(sys.argv[1:])        