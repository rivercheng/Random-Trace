from lineProcess    import processLine
from state          import State
from operation      import Ops, fromText
import sys
import os
import os.path

def dxIsCommon(dx):
    return dx == 0

def dyIsCommon(dy):
    #return -4 <= dy <= 4
    return dy == 0

def dzIsCommon(dz):
    return 2 <= dz <= 15
    #return dz == 5

def axIsCommon(ax):
    #return ax <= 20 or ax >= 340
    return ax == 0

def azIsCommon(az):
    return az == 0

def convertOps(ops, s):
    if ops == Ops.moveRight:
        if s.dx >= 0:
            return "x_leave"
        else:
            return "x_back"
    elif ops == Ops.moveLeft:
        if s.dx <= 0:
            return "x_leave"
        else:
            return "x_back"
    elif ops == Ops.moveUp:
        if s.dy >= 0:
            return "y_leave"
        else:
            return "y_back"
    elif ops == Ops.moveDown:
        if s.dy <= 0:
            return "y_leave"
        else:
            return "y_back"
    elif ops == Ops.zoomIn:
        if s.dz <= 5:
            return "z_leave"
        else:
            return "z_back"
    elif ops == Ops.zoomOut:
        if s.dz >= 5:
            return "z_leave"
        else:
            return "z_back"
    elif ops == Ops.rotateXf:
        if s.ax > 180 or s.ax == 0:
            return "ax_leave"
        else:
            return "ax_back"
    elif ops == Ops.rotateXb:
        if s.ax < 180:
            return "ax_leave"
        else:
            return "ax_back"
    elif ops == Ops.rotateYleft:
        if s.ay > 180 or s.ay == 0:
            return "ay_leave"
        else:
            return "ay_back"
    elif ops == Ops.rotateYright:
        if s.ay < 180:
            return "ay_leave"
        else:
            return "ay_back"
    elif ops == Ops.rotateZclock:
        if s.az < 180:
            return "az_leave"
        else:
            return "az_back"
    elif ops == Ops.rotateZantiClock:
        if s.az > 180 or s.az == 0:
            return "az_leave"
        else:
            return "az_back"
    else:
        return ops

if len(sys.argv) < 2:
    print "Usage: "+sys.argv[0]+" <path>"
    sys.exit()

path = sys.argv[1]
countDict = {}
probDict =  {}

totalCount = 0

s = State(396.009)

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
            type = (dxIsCommon(s.dx), dyIsCommon(s.dy), dzIsCommon(s.dz), axIsCommon(s.ax), azIsCommon(s.az), s.lastOp)
            countDict[type] = countDict.get(type, 0) + 1
            probDict[type] = probDict.get(type, {})
            newops = convertOps(ops, s)
            probDict[type][newops] = probDict[type].get(newops, 0) + 1
            
            s.transition(ops)
            totalCount += 1
    s.init()

print totalCount
print
print
res = []
for k in countDict:
    res.append((countDict[k], k))

res.sort(reverse = True)
for item in res:
    print item[1], item[0], item[0]*1.0/totalCount
    for k in probDict[item[1]]:
        print k, probDict[item[1]][k], probDict[item[1]][k] * 1.0 / item[0]





