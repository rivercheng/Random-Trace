#!/usr/bin/env python
from __future__ import with_statement
import numpy as np
import matplotlib.pyplot as plt
import cPickle
import sys

if len(sys.argv) < 3:
    print "Usage: " + sys.argv[0] + " <pickle file 1> <pickle file 2>"
    sys.exit()

with open(sys.argv[1]) as input:
    beginDict1  = cPickle.load(input)
    popularity1 = cPickle.load(input)

with open(sys.argv[2]) as input:
    beginDict2  = cPickle.load(input)
    popularity2 = cPickle.load(input)

for axis in popularity1:

    mergeDict = {}
    for v in popularity1[axis]:
        prop1 = popularity1[axis][v]
        prop2 = popularity2[axis].get(v, 0)
        mergeDict[v] = (prop1, prop2)

    for v in popularity2[axis]:
        if v not in mergeDict:
            mergeDict[v] = (0, prop2)

    v_list = []
    prop1_list = []
    prop2_list = []

    for v in sorted(mergeDict.keys()):
        v_list.append(v)
        prop1_list.append(mergeDict[v][0])
        prop2_list.append(mergeDict[v][1])


    N = len(prop1_list)
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, prop1_list, width, color='r')

    rects2 = ax.bar(ind+width, prop2_list, width, color='y')

# add some
    ax.set_ylabel('Popularity')
    ax.set_title('Popularity of ' + axis)
    ax.set_xticks(ind+width)
    xtick_lst = []
    for v in v_list:
        if v % 2 == 0:
            xtick_lst.append(v)
        else:
            xtick_lst.append("")
    ax.set_xticklabels(xtick_lst)

    ax.legend( (rects1[0], rects2[0]), ('Original', 'Generated') )

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%0.2f'%height, ha='center', va='bottom')

    #autolabel(rects1)
    #autolabel(rects2)
    plt.savefig(axis+".eps")

