from lineProcess    import processLine
from state          import State
from operation      import Ops, fromText
import sys
import os
import os.path

if len(sys.argv) < 2:
    print "Usage: "+sys.argv[0]+" <path>"
    sys.exit()

path = sys.argv[1]
x_count = {}
y_count = {}
z_count = {}
ax_count = {}
ay_count = {}
az_count = {}

s = State(396.009)

def addCount(dict, k):
    dict[k] = dict.get(k, 0) + 1

def sortCountList(dict):
    toBeSort = []
    for k in dict:
        toBeSort.append((dict[k], k))
    toBeSort.sort(reverse = True)
    return toBeSort

totalCount = 0

def printSortedList(lst):
    accu = 0
    for item in lst:
        accu += item[0] * 1.0 / totalCount
        print item[1], item[0], item[0] * 1.0 / totalCount, accu
    print
    print



for name in os.listdir(path):
    if "behavior" not in name:
        continue
    fullname = os.path.join(path, name)
    f = open(fullname, "r")
    for line in f:
        time, operation = processLine(line)
        try:
            ops = fromText(operation)
        except KeyError:
            ops = None
        if ops:
            tup = s.toTuple()
            addCount(x_count, tup[0])
            addCount(y_count, tup[1])
            addCount(z_count, tup[2])
            addCount(ax_count, tup[3])
            addCount(ay_count, tup[4])
            addCount(az_count, tup[5])
            s.transition(ops)
            totalCount += 1
    s.init()

print totalCount
print
print
printSortedList(sortCountList(x_count))
printSortedList(sortCountList(y_count))
printSortedList(sortCountList(z_count))
printSortedList(sortCountList(ax_count))
printSortedList(sortCountList(ay_count))
printSortedList(sortCountList(az_count))



