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



def action_axis_cont(action, axis, f):
    cursor = query("%s, next_op"%axis, db, "last_op='%s'"%action)
    m = {}
    for res in cursor:
        v, next_op = res
        v = int(v)
        if v not in m:
            m[v] = {}
            m[v]["total"] = 0
            m[v]["continue"] = 0
            m[v]["reverse"] = 0
            m[v]["change"] = 0
        m[v]["total"] += 1
        if next_op == action:
            m[v]["continue"] += 1
        elif next_op == reverse_acts[action]:
            m[v]["reverse"] += 1
        else:
            m[v]["change"] += 1
    
    total = 0
    first = 0
    second = 0
    diff   = 0

    for v in sorted(m.keys()):
        ma = m[v]
        print >>f, v, ma["total"], ma["continue"], ma["reverse"], ma["change"],
        if ma["total"] > 0:
            print >>f,  ma["continue"] * 1.0 / ma["total"],
            print >>f,  ma["reverse"]  * 1.0 / ma["total"],
            print >>f,  ma["change"]  * 1.0 / ma["total"]

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage " + sys.argv[0] + "<db name> <output file>"
        sys.exit()
    conn = sqlite3.connect(sys.argv[1])
    db = "behavior"
    
    actions = ( "MOVE_LEFT", "MOVE_RIGHT", "MOVE_UP", "MOVE_DOWN", "ZOOM_IN", "ZOOM_OUT",
               "TILT_FORWARD", "TILT_BACKWARD", "REVOLVE_CLOCKWISE", "REVOLVE_ANTICLOCKWISE",
               "ROTATE_CLOCKWISE", "ROTATE_ANTICLOCKWISE")
    
    reverse_acts = {"MOVE_LEFT" : "MOVE_RIGHT", "MOVE_UP":"MOVE_DOWN", "ZOOM_IN":"ZOOM_OUT",\
            "TILT_FORWARD":"TILT_BACKWARD", "REVOLVE_CLOCKWISE":"REVOLVE_ANTICLOCKWISE",\
            "ROTATE_CLOCKWISE":"ROTATE_ANTICLOCKWISE"}
    
    for key, value in list(reverse_acts.iteritems()):
        reverse_acts[value] = key

    action = "ZOOM_IN"
    axis   = "z"
    f      = open(sys.argv[2], 'w')
    action_axis_cont(action, axis, f)
    
    print >>f
    action = "REVOLVE_ANTICLOCKWISE"
    axis   = "ay"
    action_axis_cont(action, axis, f)
    
    print >>f, 'x'
    action = "REVOLVE_ANTICLOCKWISE"
    axis   = "x"
    action_axis_cont(action, axis, f)
    
    print >>f, 'y'
    action = "REVOLVE_ANTICLOCKWISE"
    axis   = "y"
    action_axis_cont(action, axis, f)
    
    print >>f, 'z'
    action = "REVOLVE_ANTICLOCKWISE"
    axis   = "z"
    action_axis_cont(action, axis, f)
    
    print >>f, 'ax'
    action = "REVOLVE_ANTICLOCKWISE"
    axis   = "ax"
    action_axis_cont(action, axis, f)
    
    print >>f, 'az'
    action = "REVOLVE_ANTICLOCKWISE"
    axis   = "az"
    action_axis_cont(action, axis, f)
    
    print >>f
    action = "REVOLVE_CLOCKWISE"
    axis   = "ay"
    action_axis_cont(action, axis, f)
    
    print >>f
    action = "MOVE_UP"
    axis   = "y"
    action_axis_cont(action, axis, f)








    


 


