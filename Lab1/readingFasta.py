#!/usr/local/bin/python

import os.path


counter = 0
accesions = ''
name = raw_input("Enter the name of the file: ")

if ( os.path.isfile(name) == False):
   print "The file does not exist";
else:
   file = open(name, 'r')
   
   for line in file:
      
      if (">" in line):
         counter += 1;
         i = 1
         exit = False
         
         while ( (exit == False) and (i < len(line)) ):
            if (line[i] == " "):
               exit = True
               accesions += '\n'
            else:
               accesions +=  line[i]
            i = i + 1
      
print counter
print accesions

file.close()
