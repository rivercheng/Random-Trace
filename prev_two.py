from __future__ import with_statement
import sqlite3
import sys
import cPickle
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
    
    actions = ( "MOVE_LEFT", "MOVE_RIGHT", "MOVE_UP", "MOVE_DOWN", "ZOOM_IN", "ZOOM_OUT",
               "TILT_FORWARD", "TILT_BACKWARD", "REVOLVE_CLOCKWISE", "REVOLVE_ANTICLOCKWISE",
               "ROTATE_CLOCKWISE", "ROTATE_ANTICLOCKWISE")

    print "Considering two previous actions"
    cursor = query("last_last_op, last_op, next_op", db)
    m = {}
    for res in cursor:
        last_last_op, last_op, next_op = res
        if (last_last_op, last_op) not in m:
            m[(last_last_op, last_op)] = {}
            m[(last_last_op, last_op)]["total"] = 0
            m[(last_last_op, last_op)]["continue"] = 0
        m[(last_last_op, last_op)]["total"] += 1
        m[(last_last_op, last_op)][next_op] = m[(last_last_op, last_op)].get(next_op, 0) + 1
        if next_op == last_op:
            m[(last_last_op, last_op)]["continue"] += 1
    total = 0
    first = 0
    second = 0
    diff   = 0

    for k,v in m.iteritems():
        #k: (last_last_op, last_op); v: map: 'total', next_op, 'continue'
        count_array = []
        for k2, v2 in v.iteritems():
            #k2: "total", "continue", and all the next actions.
            if k2 != "continue":
                count_array.append((v2, k2))
        count_array.sort(reverse=True)
        if count_array:
            #total is in the first position
            total += count_array[0][0]
            #the largest next_op is in the second position
            first += count_array[1][0]
        if len(count_array) > 2:
            second += count_array[2][0]
        
        #k[1] is the last op
        #We count how many times the same action does not have the highest probability
        if count_array[1][1] != k[1] and k[1] in actions and count_array[1][1] in actions:
            print k[1], count_array[1][1], count_array[0][0]
            diff += 1

    print total, first, first+second, first * 1.0 / total, (first+second) * 1.0 /total
    print diff

    #for k, v in m.iteritems():
    #    print k[0], k[1], v["total"], v["continue"],
    #    if v["total"] > 10:
    #        print v["continue"] * 1.0 / v["total"]
    #    else:
    #        print
    output_file = open("prev_2_output", 'w')
    for last_op in actions:
        for last_last_op in actions:
          try:
            v = m[(last_last_op, last_op)]
            print last_last_op, last_op, v["total"], v["continue"],
            if v["total"] >= 10:
                print v["continue"] * 1.0 / v["total"]
            else:
                print
          except KeyError:
              print last_last_op, last_op, 0, 0


    output_file = open(sys.argv[2], 'w')
    for last_op in actions:
        for last_last_op in actions:
          try:
            v = m[(last_last_op, last_op)]
            if v["total"] > 10:
                print >>output_file, v["continue"] * 1.0 / v["total"],
            else:
                print >>output_file, 0,
          except KeyError:
              print >>output_file, 0,
        print >>output_file










    


 


