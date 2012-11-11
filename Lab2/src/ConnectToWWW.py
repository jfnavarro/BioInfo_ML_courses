'''
Created on Nov 16, 2010

@author: jose
'''
from Bio import Entrez
import os
from Bio import SeqIO


class connectToWWW(object):

    def __init__(self):
        '''
        Constructor
        '''
        
    def connect(self):
        
        Entrez.email = "jfn@kth.se"     # Always tell NCBI who you are
        filename = "gi_186972394.gbk"
        if not os.path.isfile(filename):
            print "Downloading..."
            net_handle = Entrez.efetch(db="genome",id="186972394",rettype="gb")
            out_handle = open(filename, "w")
            out_handle.write(net_handle.read())
            out_handle.close()
            net_handle.close()
            print "Saved"

            print "Parsing..."
            record = SeqIO.read(filename, "genbank")
            print record
            

