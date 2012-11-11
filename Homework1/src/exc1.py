#! /usr/bin/env python

import sys
handle = open('./' + sys.argv[1])
matrix = list()
regulated = list()
regulators = list()
lines = 0
for i in handle:
    if '#' not in i:
        lines+=1
        matrix.append(list(i.split('\t')[0:7]))
        #print list(i.split('\t')[0:7])

################## Get a list with internal node and output nodes ####################
for i in matrix:
    regulated_gene = True
    for j in matrix:
        if i[3] == j[4]:
            regulated_gene = False
            if i[3] not in regulators:
                regulators.append(i[3])
#           print regulated_gene
        if regulated_gene and i[3] not in regulated:
            regulated.append(i[3])

################### Get list of interactions between internal and output nodes #######

links = dict()
interaction = ''
#link_type = list()
signs = dict()


for i in regulated:
    for j in matrix:
        if j[3] == i:
            key = j[1] + '\t' + i;
        if key not in links:
            links[key] = [j[5]]
        else:
            links[key] =  links[key] + [j[5]]

############### Number of links from internal to output #############
for i in regulated:
    for j in matrix:
        if j[3] == i:
            if j[5] not in signs:
                signs[j[5]] = 1
            else:
                signs[j[5]]+=1


############## Number of links between internal links #############
inter_signs = dict()

for i in regulators:
    for j in matrix:
        if j[1] == i:
            if j[5] not in inter_signs:
                inter_signs[j[5]] = 1
            else:
                inter_signs[j[5]]+=1


print "N*: ", len(regulators)
print "N^out:", len(regulated)
print "M*: ", inter_signs
print "M^out: ", signs
print lines
'''
for k,v in links.iteritems():
    print k,v
'''

handle.close()

