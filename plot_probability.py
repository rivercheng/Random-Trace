#!/usr/bin/env python
from __future__ import with_statement
import numpy as np
import matplotlib.pyplot as plt
import cPickle
import sys

if len(sys.argv) < 3:
    print "Usage: " + sys.argv[0] + "<pickle file 1> <output filename> [n = 1]"
    print "\tIn this pickle file: a list of probability list (m*n), \n\ta list of name of actions (n),\n\tand a list of label (m)"
    sys.exit()

count = 1
if len(sys.argv) > 3:
    count = int(sys.argv[3])


input =  open(sys.argv[1])

fig = plt.figure()

for i in range(count):
    prob_list_list  = cPickle.load(input)
    name_list       = cPickle.load(input)
    label_list      = cPickle.load(input)
    mse             = cPickle.load(input)

    assert(len(prob_list_list) == len(label_list))
    assert(len(prob_list_list[0]) == len(name_list))

    m = len(name_list)
    n = len(label_list)

    ind = np.arange(m)  # the x locations for the groups
    width = 0.35       # the width of the bars

    #fig = plt.figure()
    ax = fig.add_subplot(5, 5, i+1)
    #ax.set_ylabel('Popularity', size=5)
    rects1 = ax.bar(ind, prob_list_list[0], width, color='r')
    rects2 = ax.bar(ind+width, prob_list_list[1], width, color='y')

    #ax.set_title('Popularity of ' + axis)
    ax.set_xticks(ind+width)
    xtick_lst = []
    for name in name_list:
        xtick_lst.append(name)
    ax.set_xticklabels(xtick_lst, size=5)

    #ax.legend( (rects1[0], rects2[0]), ('Original', 'Generated') , size=5)
    ax.set_ylim(0,1)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(5)

    #def autolabel(rects):
        # attach some text labels
    #    for rect in rects:
    #        height = rect.get_height()
    #        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%0.2f'%height, ha='center', va='bottom')

    #autolabel(rects1)
    #autolabel(rects2)
plt.savefig(sys.argv[2]+'.pdf')

