from __future__ import with_statement
import sqlite3
import sys
import pylab
MIN_DURATION = 0

def query(column, db, condition=None):
    query_str = "SELECT "+column+" FROM "+db
    if (condition is not None):
        query_str += " WHERE "+condition
    #print query_str
    return  conn.execute(query_str)

def prob(m, v, total):
    return m[v] * 1.0 / total

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage " + sys.argv[0] + "<db name> <output file>"
        sys.exit()
    conn = sqlite3.connect(sys.argv[1])
    db = "behavior"
    
    actions = ( "MOVE_LEFT", "MOVE_RIGHT", "MOVE_UP", "MOVE_DOWN", "ZOOM_IN", "ZOOM_OUT",
               "TILT_FORWARD", "TILT_BACKWARD", "REVOLVE_CLOCKWISE", "REVOLVE_ANTICLOCKWISE",
               "ROTATE_CLOCKWISE", "ROTATE_ANTICLOCKWISE")

    cursor = query("x, y, z, ax, ay, az", db)
    m = {}
    mx = {}
    my = {}
    mz = {}
    max = {}
    may = {}
    maz = {}
    total = 0
    for res in cursor:
        x, y, z, ax, ay, az = map(int, res)
        if x == 0 and y == 0 and z < 10 and ax == 0 and ay == 0 and az == 0:
            continue
        m[(x, y, z, ax, ay, az)] = m.get((x, y, z, ax, ay, az), 0) + 1
        mx[x] = mx.get(x, 0) + 1
        my[y] = my.get(y, 0) + 1
        mz[z] = mz.get(z, 0) + 1
        max[ax] = max.get(ax, 0) + 1
        may[ay] = may.get(ay, 0) + 1
        maz[az] = maz.get(az, 0) + 1
        total += 1

    #revise the probability of z value. Remove the effect of default viewpoint
    left = mz[3]
    right = mz[-1]
    diff  = mz[3] - mz[-1]
    #mz[2] = mz[-1] + diff * 3. /4.
    #mz[1] = mz[-1] + diff * 2. /4.
    #mz[0] = mz[-1] + diff * 1. /4.

    f_out = open(sys.argv[2], 'w')
    for x in mx:
        print >>f_out, x, mx[x]
    print >>f_out
    for y in my:
        print >>f_out, y, my[y]
    print >>f_out
    for z in mz:
        print >>f_out, z, mz[z]
    print >>f_out
    for ax in max:
        print >>f_out, ax, max[ax]
    print >>f_out
    for ay in may:
        print >>f_out, ay, may[ay]
    print >>f_out
    for ax in maz:
        print >>f_out, az, maz[az]
    print >>f_out

    count_vp_lst = []
    for vp, count in m.iteritems():
        x, y, z, ax, ay, az = vp
        if x == 0 and y == 0 and z < 10 and ax == 0 and ay == 0 and az == 0:
            continue
        count_vp_lst.append((count, vp))
    count_vp_lst.sort(reverse=True)
    
    prob_real_lst = []
    prob_est_lst = []
    for count, vp in count_vp_lst:
        x, y, z, ax, ay, az = vp
        print vp,
        probreal = count * 1.0 / total, 
        probest  =  prob(mx, x, total) * prob(my, y, total) * prob(mz, z, total) * prob(max, ax, total) * prob(may, ay, total) * prob(maz, az, total)
        print probreal, probest
        prob_real_lst.append(probreal)
        prob_est_lst.append(probest)

    pylab.plot(prob_real_lst[:1000])
    pylab.plot(prob_est_lst[:1000])
    pylab.show()

        







    


 


