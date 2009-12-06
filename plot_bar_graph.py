#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

#Continue Probability for 9 meshes
def plot_continue_probability():
    probs = []
    names = []
    file = open("continue_probability_9")
    for line in file:
        name, prob = line.split()
        names.append(name)
        probs.append(float(prob))
    N = len(probs)

    ind = np.arange(N)
    width = 0.7

    fig = plt.figure()
    ax  = fig.add_subplot(111)
    rect = ax.bar(ind, probs, width)

    ax.axis(ymin=0, ymax=1)
    ax.set_ylabel('Probability of Continue')
    ax.set_xticks(ind+0.5*width)
    ax.set_xticklabels(names, fontsize='small')

    autolabel(ax, rect)
    plt.savefig('cont_prob_9.eps')

def autolabel(ax, rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 
                    1.01*height, '%0.3f'%height,
                    ha='center', va='bottom')


if __name__ == "__main__":
    plot_continue_probability()




