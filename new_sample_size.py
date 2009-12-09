from __future__ import with_statement
import sqlite3
import sys
import cPickle
import pylab
MIN_DURATION = 0

def query(column, db, condition=None):
    query_str = "SELECT "+column+" FROM "+db
    if (condition is not None):
        query_str += " WHERE "+condition
    #print query_str
    return  conn.execute(query_str)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage " + sys.argv[0] + "<db name> <output file>"
        sys.exit()
    conn = sqlite3.connect(sys.argv[1])
    db = "behavior"
    Threshold = 10

    cursor = query("x, y, z, ax, ay, az, last_op, next_op", db)
    m = {}
    for res in cursor:
        x, y, z, ax, ay, az = map(int, res[:6])
        last_op, next_op    = res[6:]
        if last_op in ["MOVE_LEFT", "MOVE_RIGHT"]:
            m[(x, last_op)] = m.get((x, last_op), 0) + 1
        elif last_op in ["MOVE_UP", "MOVE_DOWN"]:
            m[(y, last_op)] = m.get((y, last_op), 0) + 1
        elif last_op in ["ZOOM_IN", "ZOOM_OUT"]:
            m[(z, last_op)] = m.get((z, last_op), 0) + 1
        elif last_op in ["TILT_FORWARD", "TILT_BACKWARD"]:
            m[(ax, last_op)] = m.get((ax, last_op), 0) + 1
        elif last_op in ["REVOLVE_ANTICLOCKWISE", "REVOLVE_CLOCKWISE"]:
            m[(ay, last_op)] = m.get((ay, last_op), 0) + 1
        elif last_op in ["ROTATE_ANTICLOCKWISE", "ROTATE_CLOCKWISE"]:
            m[(az, last_op)] = m.get((az, last_op), 0) + 1

    lst = []
    for state, count in m.iteritems():
        lst.append((count, state))

    lst.sort(reverse=True)
    count_lst = [count for (count, s) in lst]
    total_count = len(count_lst)
    valid_lst = [x for x in count_lst if x > 10]
    valid_count = len(valid_lst)

    for count, s in lst:
        print s, count

    pylab.semilogy(count_lst)
    pylab.semilogy([valid_count, valid_count], [1,10], color='black')
    pylab.semilogy([0,valid_count], [10, 10], color='black')
    pylab.text(valid_count, 0.8, "%d"%valid_count)
    pylab.text(total_count, 0.8, "%d"%total_count)
    pylab.ylabel("Count of Occurence")
    pylab.xlim(0, total_count)
    pylab.xlabel("Rank")
    #pylab.yticks([0,1,2,3],[0,1,10,100,1000])
    pylab.savefig(sys.argv[2])










    


 


