#!/usr/local/bin/python

import os.path

codontable = dict(TTT="F", TTC="F", TTA="L", TTG="L",
             TCT="S", TCC = "S", TCA="S", TCG="S",
             TAT="Y", TAC ="Y", TAA="Stop", TAG="Stop",
             TGT="C", TGC="C", TGA="Stop", TGG="W",
             CTT="L", CTC="L", CTA="L", CTG="L",
             CCT="P", CCC="P", CCA="P", CCG="P",
             CAT="H", CAC="H", CAA="Q", CAG="Q",
             CGT="R", CGC="R", CGA="R", CGG="R",
             ATT="I", ATC="I", ATA="I", ATG="M",
             ACT="T", ACC="T", ACA="T", ACG="T",
             AAT="N", AAC="N", AAA="K", AAG="K",
             AGT="S", AGC="S", AGA="R", AGG="R",
             GTT="V", GTC="V", GTA="V", GTG="V",
             GCT="A", GCC="A", GCA="A", GCG="A",
             GAT="D", GAC="D", GAA="E", GAG="E",
             GGT="G", GGC="G", GGA="G", GGG="G");
counter = 0
output = ''

def protein(chain):
    for rna, aa in codontable.iteritems():
        if (chain == rna):
            return aa    
    return 'N'

def removeCrapp(chain):
    if (chain.find(" ") != -1):
        return chain[0:chain.find(" ")] + chain[chain.find("\n"):len(chain)]
    else:
        return chain

name = raw_input("Enter the name of the file: ")

if ( os.path.isfile(name) == False):
   print "The file does not exist";
else:
   file = open(name, 'r')
   
   for line in file:
       if (">" in line):
           output += removeCrapp(line)
       else:
           
           i = 0
           exit = False
         
           while ( (exit == False) and (i < len(line)) ):
               temp = line[i*3:(i*3)+3]
               if(temp.find("\n") == -1):
                   codon = protein(temp)
                   if( codon == "Stop"):
                       output += "X"
                   else:
                       output += codon
               else:
                   output += '\n'
                   exit = True
                   
               i = i + 1         


print output
file.close()  