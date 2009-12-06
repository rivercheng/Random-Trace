import pylab
import numpy as np
import sys
#
# define some sizes of the scatter marker
#
if len(sys.argv) < 3:
    print "Usage: ", sys.argv[0], " <input file> <output file>"
    sys.exit()

input = open(sys.argv[1])
cont_probs = []
for line in input:
    probs = [float(x) for x in line.split()]
    cont_probs.append(probs)

actions= ('ML','MR','MU','MD','ZI','ZO','TF','TB','REAN', 'REC', 'ROAN', 'ROC')

for i in range(12):
    for j in range(12):
        if cont_probs[i][j] > 0:
            pylab.scatter([j+1], [i+1], marker = 'o', s = cont_probs[i][j]*1000, facecolor='white')
            #pylab.text(j+1, i+1, "%0.3f"%cont_probs[i][j], ha='center', va='center', fontsize='small')
        else:
            pylab.scatter([j+1], [i+1], marker = 'x', s = 100, facecolor = 'white')

pylab.axis([0, 12, 0, 12])
pylab.yticks(range(1, 14), actions)
pylab.xticks(range(1, 14), actions)
pylab.xlabel('Second Latest Action')
pylab.ylabel('Latest Action')
pylab.title('The Probability of Continue Action')
pylab.grid()
pylab.savefig(sys.argv[2])
