#! /usr/bin/env python

from Bio import SeqIO
import sys

usage = """
Usage: faTosto <infile> [<outfile>]

If no output file is given on the command line, a filename is
created from the input filename by appending '.sthlm'.
"""


nargs = len(sys.argv)
if  nargs < 2 or nargs > 3:
	sys.stderr.write(usage)
	sys.exit(1)

fname = sys.argv[1]
oname = fname + '.sthlm'		# Tentative output filename
if nargs == 3:
	oname = sys.argv[2]
try:
	SeqIO.convert(fname, 'fasta', oname, 'stockholm');
except IOError, (errno, strerror):
	print >> sys.stderr, "I/O error(%s): %s" % (errno, strerror)
except:
	print >> sys.stderr, "An error occured. "

exit(0)

