#!/usr/local/bin/python

import random

length = int(raw_input("Please enter the longitude of the chain: "));
dna = ""

if( length < 0):
    print "Invalid Number"
else:
    for x in range(length):
        dna += random.choice('ACGT');

print "myrandomsequence"
print dna