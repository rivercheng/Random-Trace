#!/usr/bin/env python
from readTrace      import processLine, parseFiles
from state          import State
from operation      import Ops, fromText, axisOfAction, directionOfAction
import sys
import os
import os.path

if len(sys.argv) < 2:
    print "Usage: "+sys.argv[0]+" <path>"
    sys.exit()

path = sys.argv[1]

count = [{}, {}, {}, {}, {}, {}]
continueDictF = [{}, {}, {}, {}, {}, {}]
reverseDictF = [{}, {}, {}, {}, {}, {}]
continueDictB = [{}, {}, {}, {}, {}, {}]
reverseDictB = [{}, {}, {}, {}, {}, {}]
changeDict = [{}, {}, {}, {}, {}, {}]
forwardDict = [{}, {}, {}, {}, {}, {}]
backwardDict = [{}, {}, {}, {}, {}, {}]

s = State(396.009)
prev_time = 0

for time, operation in parseFiles(path):
    if operation == "BEGIN":
        s.init()
        prev_time = time
    duration = time - prev_time
    prev_time = time
    try:
        ops = fromText(operation)
    except KeyError:
        ops = None
    if ops:
        tup = s.toTuple()
        #count the coordinates for each axis
        for i in range(6):
            count[i][tup[i]] = count[i].get(tup[i], 0) + 1

        try:
            axis = axisOfAction(tup[6])
            axisN = axisOfAction(ops)
            if ops == tup[6]:
                if directionOfAction(ops) > 0:
                    continueDictF[axis][tup[axis]] = continueDictF[axis].get(tup[axis], 0) + 1
                else:
                    continueDictB[axis][tup[axis]] = continueDictB[axis].get(tup[axis], 0) + 1
            elif axis == axisN:
                if directionOfAction(ops) > 0:
                    reverseDictF[axis][tup[axis]] = reverseDictF[axis].get(tup[axis], 0) + 1
                else:
                    reverseDictB[axis][tup[axis]] = reverseDictB[axis].get(tup[axis], 0) + 1
            else:
                changeDict[axis][tup[axis]] = changeDict[axis].get(tup[axis], 0) + 1
                if directionOfAction(ops) > 0:
                    forwardDict[axisN][tup[axisN]] = forwardDict[axisN].get(tup[axisN], 0) + 1
                else:
                    backwardDict[axisN][tup[axisN]] = backwardDict[axisN].get(tup[axisN], 0) + 1
        except KeyError:
            pass
        s.transition(ops)

for i in range(6):
    print count[i]
print 
for i in range(6):
    print "continueF",
    print continueDictF[i]
    print "continueB",
    print continueDictB[i]
    print "reverseF",
    print reverseDictF[i]
    print "reverseB",
    print reverseDictB[i]
    print "change",
    print changeDict[i]
