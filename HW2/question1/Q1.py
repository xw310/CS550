#!/usr/bin/env python3
#-*-coding:utf-8-*-
'''
svd decomposition for CS550 HW2
'''

from scipy import linalg
import numpy as np
#(a)
M = [[1,2],[2,1],[3,4],[4,3]]
M = np.array(M)

U, s, VT = linalg.svd(M, full_matrices=False);
print (f"U is \n {U}")
print (f"s is \n {s}")
print (f"VT is \n {VT}")

#(b)
N = np.dot(M.T, M)
Evals_origin, Evecs_origin = linalg.eigh(N)

l = [[Evals_origin[i],Evecs_origin.T[i]] for i in range(len(Evals_origin))]
l.sort(key = lambda X: X[0], reverse = True)

Evals = []
Evecs = []

for i in range(len(l)):
    Evals.append(l[i][0])
    Evecs.append(l[i][1])

Evecs = np.transpose(np.array(Evecs))

print (f"Evals is \n {Evals}")
print (f"Evecs is \n {Evecs}")
