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
count = {}
actionCount = {}
action = {}

s = State(396.009)

prev_time = 0

for name in os.listdir(path):
    if "behavior" not in name:
        continue
    fullname = os.path.join(path, name)
    f = open(fullname, "r")
    for line in f:
        time, operation = processLine(line)
        duration = time - prev_time
        prev_time = time
        try:
            ops = fromText(operation)
        except KeyError:
            ops = None
        if ops:
            tup = s.toTuple()
            count[tup] = count.get(tup, 0) + 1
            
            ac = actionCount.get(tup, {})
            ac[ops] = ac.get(ops,0) + 1
            actionCount[tup] = ac

            if tup not in action:
                action[tup] = [(ops, duration)]
            else:
                action[tup].append((ops, duration))
            s.transition(ops)
    s.init()
    prev_time = 0

print s.range()

toBeSort = []
toBeSort2 = []
for k in count:
    toBeSort.append((count[k], k))
    toBeSort2.append((len(actionCount[k]), k))
toBeSort.sort(reverse = True)
toBeSort2.sort(reverse = True)

for i in range(len(toBeSort)):
    print toBeSort[i][0], toBeSort2[i][0]

