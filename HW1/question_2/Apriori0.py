#!/usr/bin/env python3
#-*-coding:utf-8-*-
#03/02/2019
'''
Apriori algorithm for CS550 HW1 question2
'''

import sys
import itertools

class Apriori():

    def __init__(self,support):
        self.items_single = {}
        self.items_double = {}
        self.items_triple = {}
        self.support = support

    def loadfile(self,file):
        fp = open(file, 'r')
        for line in fp:
            yield line.strip().split()

    def get_single(self,file):
        for line in self.loadfile(file):
            for item in line:
                if item not in self.items_single:
                    self.items_single.setdefault(item,1)
                else:
                    self.items_single[item] += 1

        for key in list(self.items_single):
            if self.items_single[key] < self.support:
                del self.items_single[key]

    def get_double(self,file):
        '''In this step, we do not generate doubles according to singles,\
         we generate through input file to save one step'''
        for line in self.loadfile(file):
            if len(line) < 2:    #if len<2, then no doubles
                continue
            for i in range(len(line)):
                if line[i] in self.items_single and self.items_single[line[i]] >= self.support:
                    for j in range(i+1,len(line)):
                        if line[j] in self.items_single and self.items_single[line[j]] >= self.support:
                            l = sorted([line[i], line[j]])
                            #print(l)
                            #input()
                            self.items_double.setdefault(l[0], {})
                            self.items_double[l[0]].setdefault(l[1], 0)
                            self.items_double[l[0]][l[1]] += 1

        for key in list(self.items_double):
            for key1 in list(self.items_double[key]):
                if self.items_double[key][key1] < self.support:
                    del self.items_double[key][key1]

    def get_triple(self,file):
        '''    '''
        for line in self.loadfile(file):
            if len(line) < 3:    #if len<3, then no triples
                continue
            for i in range(len(line)):
                if line[i] in self.items_single and self.items_single[line[i]] >= self.support:
                    for j in range(i+1,len(line)):
                        if line[j] in self.items_single and self.items_single[line[j]] >= self.support:
                            for k in range(j+1,len(line)):
                                if line[j] in self.items_single and self.items_single[line[j]] >= self.support:
                                    l = sorted([line[i], line[j], line[k]])
                                    #print(l)
                                    #input()
                                    self.items_triple.setdefault(l[0], {})
                                    self.items_triple[l[0]].setdefault(l[1], {})
                                    self.items_triple[l[0]][l[1]].setdefault(l[2], 0)
                                    self.items_triple[l[0]][l[1]][l[2]] += 1
        #print(self.items_triple)
        #input()
        #prune the unfrequent triples
        for key in list(self.items_triple):
            for key1 in list(self.items_triple[key]):
                for key2 in list(self.items_triple[key][key1]):
                    if self.items_triple[key][key1][key2] < self.support:
                        del self.items_triple[key][key1][key2]

    def association_rule_double(self):
        confidence = []
        for key in self.items_double:
            for key1 in self.items_double[key]:
                confidence.append([key,key1,self.items_double[key][key1]/self.items_single[key]])
                confidence.append([key,key1,self.items_double[key][key1]/self.items_single[key1]])
        confidence = sorted(confidence, key=lambda x: x[1])
        confidence = sorted(confidence, key=lambda x: x[0])
        confidence = sorted(confidence, key=lambda x: x[2],reverse = True)
        confidence = confidence[:5]

        for double in confidence:
            print(double[0],'\t',double[1],'\t\t',double[2])

    def association_rule_triple(self):
        confidence = []
        for key in self.items_triple:
            for key1 in self.items_triple[key]:
                for key2 in self.items_triple[key][key1]:
                    confidence.append([key,key1,key2,self.items_triple[key][key1][key2]/self.items_double[key][key1]])
                    confidence.append([key,key2,key1,self.items_triple[key][key1][key2]/self.items_double[key][key2]])
                    confidence.append([key1,key2,key,self.items_triple[key][key1][key2]/self.items_double[key1][key2]])
        confidence = sorted(confidence, key=lambda x: x[2])
        confidence = sorted(confidence, key=lambda x: x[1])
        confidence = sorted(confidence, key=lambda x: x[0])
        confidence = sorted(confidence, key=lambda x: x[3],reverse = True)
        confidence = confidence[:5]

        for triple in confidence:
            print(triple[0],'+',triple[1],'\t',triple[2],'\t\t',triple[3])

if __name__ == '__main__':

    script, log  = sys.argv
    f = open(log,'w')
    __con__ = sys.stdout
    sys.stdout = f

    apriori = Apriori(100)
    apriori.get_single('browsing.txt')
    #print(apriori.items_single)
    print('get_single finished',file = __con__)
    apriori.get_double('browsing.txt')
    #print(apriori.items_double)
    print('get_double finished',file = __con__)

    apriori.association_rule_double()
    print('association_rule_double finished',file = __con__)

    print('\ndividing line **************************** \n')
    apriori.get_triple('browsing.txt')
    #print(apriori.items_triple)
    print('get_triple finished',file = __con__)

    apriori.association_rule_triple()
    print('association_rule_triple finished',file = __con__)
