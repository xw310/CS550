#!/usr/bin/env python2
#-*-coding:utf-8-*-
'''
Page rank algorithm for CS550 HW2 question3
'''
import numpy as np

class PageRank():

    def __init__(self,n:int):
        '''Initialization '''
        self.n = n
        self.M = np.zeros((n,n))

    def load_file(self,file):
        '''load file '''
        f = open(file, 'r')
        for i, line in enumerate(f):
            yield line.strip().split()

    def generate_matrix(self,file):
        '''generate matrix M according to file (during which remove the duplicates) '''
        dict = {}
        for line in self.load_file(file):
            n1,n2 = line
            dict.setdefault(n1,set())
            dict[n1].add(n2)

        for source in dict:
            count = len(dict[source])
            for destination in dict[source]:
                self.M[int(destination)-1][int(source)-1] = 1/count

    def Iteration(self, times:int, beta):
        '''iterate to compute final scores '''
        r0 = 1/self.n * np.ones((self.n,1))
        ones = (1-beta)/self.n * np.ones((self.n,1))
        for i in range(times):
            r = beta * np.dot(self.M , r0) + ones
            r0 = r
        return r

if __name__ == '__main__':
    file = 'graph.txt'
    pr = PageRank(100)
    pr.generate_matrix(file)
    r = pr.Iteration(40,0.8)

    rank = []
    for i in range(r.shape[0]):
        rank.append([r[i],i+1])
    rank.sort(key = lambda X:X[0], reverse = True)

    print('the top 5 ids with the highest PageRank score')
    for i in range(5):
        print(f'id:{rank[i][1]}, score:{rank[i][0]}')
    print('\n')

    print('the bottom 5 ids with the lowest PageRank score')
    for i in range(-1,-6,-1):
        print(f'id:{rank[i][1]}, score:{rank[i][0]}')
