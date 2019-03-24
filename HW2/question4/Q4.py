#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kmeans for CS550 HW2 question4
run this on school server unless you have java enviroment on your local system (pyspark needs this)
Before runing the script, put the data file into school server HDFS system(spark read file from hdfs system on default)
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg
from pyspark import SparkContext
import os


def mapper(line):
    '''spliting the line and then return in the form of np.array'''
    lines = line.split(' ')
    lines_list = [float(x) for x in lines]
    return np.array(lines_list)


def closest_center(row, centers):
    '''for each data, find the closest center and returned in the form (center,(data,1)) '''
    dist = [(i, linalg.norm(row - center, 2)) for i, center in enumerate(centers)]
    dist.sort(key=lambda k: k[-1])
    return (dist[0][0], (row, 1))


def cost_computing(row, centers):
    '''compute the distance between data and corresponding center '''
    ith, (d, n) = row
    dist = linalg.norm(d - centers[ith], 2)
    return dist**2


def plot_cost(c1_cost, c2_cost):
    '''plot cost as a function of loop '''
    x = range(1, len(c1_cost) + 1)

    plt.title('cost for c1&c2', fontsize=15)
    plt.xlabel('loops', fontsize=15)
    plt.ylabel('cost', fontsize=15)
    plt.plot(x, c1_cost, color='blue', linewidth=2.0, linestyle='-',label="c1_cost")
    plt.plot(x, c2_cost, color='red', linewidth=2.0, linestyle='-',label="c2_cost")
    plt.legend(loc='upper right')
    plt.show()


if __name__ == '__main__':

    loops = 20

    sc = SparkContext.getOrCreate()
    # read data
    path = '/user/xw310/CS550_HW2_data/data.txt'
    data = sc.textFile(path).map(lambda row:mapper(row)).cache()
    # read c1
    path1 = '/user/xw310/CS550_HW2_data/c1.txt'
    c1 = sc.textFile(path1).map(lambda row:mapper(row)).collect()
    # read c2
    path2 = '/user/xw310/CS550_HW2_data/c2.txt'
    c2 = sc.textFile(path2).map(lambda row:mapper(row)).collect()

    c1_cost = []
    c2_cost = []

    for i in range(loops):
        print(f'now in {i+1}th loop')
        # find the closest centroid
        kmeans_1 = data.map(lambda row: closest_center(row, c1))
        # compute the cost
        cost1 = kmeans_1.map(lambda row: cost_computing(row, c1)).sum()
        c1_cost.append(cost1)
        # re-calculate the centroids
        c1 = kmeans_1.reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1])) \
                     .map(lambda row: row[-1][0] / row[-1][1]).collect()

        # same process as above for c2
        kmeans_2 = data.map(lambda row: closest_center(row, c2))
        cost2 = kmeans_2.map(lambda row: cost_computing(row, c2)).sum()
        c2_cost.append(cost2)
        c2 = kmeans_2.reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1])) \
                     .map(lambda row: row[-1][0] / row[-1][1]).collect()

    #plot
    plot_cost(c1_cost, c2_cost)

    #compute how much cost decrease after 10 loops
    print('when using c1 as centroids, the percentage change in cost after 10 iterations is')
    print((c1_cost[0]-c1_cost[10])/c1_cost[0], '\n')

    print('when using c2 as centroids, the percentage change in cost after 10 iterations is')
    print((c2_cost[0]-c2_cost[10])/c2_cost[0], '\n')

    #print the centeroids in c1 and c2
    print('centers in c1')
    for center in c1:
        for ith in center:
            print(round(ith,2), end = '')
        print('\n')

    print('###########################')
    print('centers in c2')
    for center in c2:
        for ith in center:
            print(round(ith,2), end = '')
        print('\n')
