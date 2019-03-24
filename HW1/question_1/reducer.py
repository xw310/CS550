#!/usr/bin/env python2

#Reduce task for the Friend recommendation problem

import itertools
import sys

#script, log = sys.argv
#f = open(log,'w')
#__console__=sys.stdout
#sys.stdout = f

n_rec = 10

def add_dict(users,key1,key2,already_friend):

    users.setdefault(key1, {})
    users[key1].setdefault(key2, [1,0])
    users[key1][key2][0] += 1

    if already_friend:
        users[key1][key2][0] -= 1
        users[key1][key2][1] = 1



# input comes from STDIN (standard input)
users = {}

for line in sys.stdin:
    # remove leading and trailing whitespace
    #print line
    line = line.strip().split("\t")
    #print line
    #print(line[0].strip().split(","))
    key = tuple(map(int,line[0].strip().split(",")))
    friendFlag = int(line[1])
    key1,key2 = key
    add_dict(users,key1,key2,friendFlag)
    add_dict(users,key2,key1,friendFlag)

for k1 in users.keys():
    recommendations = []
    for k2 in users[k1].keys():
        n,flag = users[k1][k2]
        if not flag:
            recommendations.append((k2,n))
    recommendations = sorted(recommendations,key=lambda x: x[0])
    recommendations = sorted(recommendations,key=lambda x: x[1],reverse=True)
    if len(recommendations)>0:
        recommendations = list(map(str,zip(*recommendations)[0]))
        #sys.stderr = f
        print k1,'\t',','.join(recommendations[:n_rec])
