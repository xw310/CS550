#!/usr/bin/env python2
# map_friends_rec.py

#Map task for the Friend recommendation problem

import itertools
import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip().split()
    #print (line)

    key = int(line[0])
    if len(line)>1:
        friends = line[1]
        if friends!='':
            friends = line[1].split(',')
            friends = sorted(map(int,friends))
            for friend in friends:
                pair = tuple(sorted([key,friend]))    #tuple
                pair = ','.join(map(str,pair))    #map to list of string,then join as a new string
                print pair,"\t",1

            for pair in itertools.combinations(friends,2):
                pair = ','.join(map(str,pair))
                print pair,"\t",0
