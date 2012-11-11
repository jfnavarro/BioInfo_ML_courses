#!/usr/local/bin/python

import os.path

def removeCrapp(chain):
    if (chain.find(" ") != -1):
        return chain[0:chain.find(" ")] + chain[chain.find("\n"):len(chain)]
    else:
        return chain
counter = 0
output = ''
name = raw_input("Enter the name of the file: ")

if ( os.path.isfile(name) == False):
   print "The file does not exist";
else:
   file = open(name, 'r')
   
   for line in file:
       if (">" in line):
           if((len(output) > 0) and (output[len(output)-1] != "\n")):
               output += '\n' + line
           else:
               output += line
           counter = 0
       
       else:
           
           i = 0
           exit = False
         
           while ( (exit == False) and (i < len(line)) ):
               if ( (line[i] != " ") and (line[i] != '\n')  ):
                   if (counter == 59):
                       output += line[i] + '\n' 
                       counter = 0
                   else:
                       counter += 1
                       output += line[i]
               else:
                   exit = True 
                       
               i = i + 1
                  
print output

file.close()                   
     
"WikiPedia :UniProt is the Universal Protein resource, a central repository of protein" 
"data created by combining the Swiss-Prot, TrEMBL and PIR-PSD databases." 
"UniProt is based on protein sequences, many of which are derived from genome sequencing" 
"projects. It contains a large amount of information about the biological function of proteins"
"derived from the research literature."       
        
        