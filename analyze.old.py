from __future__ import with_statement
import sqlite3
import sys
import readline
MIN_DURATION = 20000

def query(column, db, condition=None):
    query_str = "SELECT "+column+" FROM "+db
    if (condition is not None):
        query_str += " WHERE "+condition
    #print query_str
    return  conn.execute(query_str)

def probability(db, condition, common=None):
    res2 = 1.0
    if common is not None:
        condition += " AND %s "%common
    res1 = query("count(*)", db, condition).next()
    res2 = query("count(*)", db, common).next()
    if res2[0] == 0:
        return None
    else:
        return res1[0] * 1.0 / res2[0]

def prob_continue(db, condition):
    if condition is not None:
        return probability(db, "last_op = next_op", "%s and duration > %d" % (condition, MIN_DURATION))
    else:
        return probability(db, "last_op = next_op", "duration > %d" % MIN_DURATION)

def prob_change(db, condition):
    if condition is not None:
        return probability(db, "last_op <> next_op", "%s and duration > %d" % (condition, MIN_DURATION))
    else:
        return probability(db, "last_op <> next_op", "duration > %d" % MIN_DURATION)

def prob_quit_reset(db, condition):
    return probability(db, "(next_op = 'QUIT' OR next_op = 'RESET')", condition)

def popularity(db, condition):
    return probability(db, condition)

def range(db, column, condition=None):
    cursor = query("DISTINCT "+column, db, condition)
    range_ = []
    for res in cursor:
        range_.append(res[0])
    return range_

def count(db, condition):
    cursor = query("COUNT(*)", db, condition)
    return cursor.next()[0]

if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    db = "behavior"
    
    cols = ("x", "y", "z", "ax", "ay", "az")
    other_cols = ("duration", )
    actions = ("ZOOM_IN", "ZOOM_OUT", "MOVE_LEFT", "MOVE_RIGHT", "MOVE_UP", "MOVE_DOWN", \
               "TILT_FORWARD", "TILT_BACKWARD", "REVOLVE_CLOCKWISE", "REVOLVE_ANTICLOCKWISE",\
               "ROTATE_CLOCKWISE", "ROTATE_ANTICLOCKWISE")

    conn.execute("create table "+ db + \
        "(x integer, y integer, z integer, \
         ax integer, ay integer, az integer, \
         last_op_index integer, next_op_index integer, \
         count integer, duration integer, \
         last_op text, next_op text)")

    with open('res', 'r') as f_input:
        for line in f_input:
            tup = line.split()
            conn.execute("insert into behavior values \
                     (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tup)
    
    for col in cols:
        conn.execute("CREATE INDEX "+ col + " ON " + db + \
                "(%s)" % col)

    for col in other_cols:
        conn.execute("CREATE INDEX "+ col + " ON " + db + \
                "(%s)" % col)

    print "The begin probability:"
    
    for act in actions:
        print act, probability(db, "next_op = '%s'" % act, \
                "next_op <> 'QUIT' AND (last_op = 'RESET' OR last_op = 'BEGIN')") 
    print



    print "Popularity:"
    
    ranges = []
    for col in cols:
        ranges.append( (col, range(db, col)) )

    for col, range_ in ranges:
        print "\tcolumn ", col, " :"
        for value in range_:
            print "\t\t%-10d" % value, "%0.6f" % popularity(db, "%s = %d" % (col, value))
    print 

    print "Percentage of Separate Pressing (duration > %s):" \
            % MIN_DURATION, "\t", probability(db, "duration > %d" % MIN_DURATION)
    print 
    
    print "General Probability of Actions:"
    general_prob = {}
    for action in (actions + ("QUIT", "RESET")):
        prob =  probability(db, "next_op = '%s'" % action, "duration > %d" % MIN_DURATION)
        general_prob[action] = prob
        if prob is not None:
            print "%30s" % action, ": ", "%0.4f" % prob
    print

    print "Change Probability:"
    print "%30s" % "General", ": ", "%0.4f" % prob_change(db, None)
    for action in actions:
        prob = prob_change(db, "last_op = '%s'" % action)
        if prob is not None:
            print "%30s" % action, ": ", "%0.4f" % prob

    print "Change to Probability:"
    change_to_prob = {}
    for action in (actions + ("QUIT", "RESET")):
        prob = probability(db, "next_op = '%s'" % action, "next_op != last_op")
        change_to_prob[action] = prob
        if prob is not None:
            print "%30s" % action, ": ", "%0.4f" % prob
    
    acts = {"x": ("MOVE_LEFT", "MOVE_RIGHT"), "y" : ("MOVE_UP", "MOVE_DOWN"), \
            "z" : ("ZOOM_IN", "ZOOM_OUT"), "ax": ("TILT_FORWARD", "TILT_BACKWARD"), \
            "ay": ("REVOLVE_CLOCKWISE", "REVOLVE_ANTICLOCKWISE"), \
            "az": ("ROTATE_CLOCKWISE", "ROTATE_ANTICLOCKWISE")}

    reverse_acts = {"MOVE_LEFT" : "MOVE_RIGHT", "MOVE_UP":"MOVE_DOWN", "ZOOM_IN":"ZOOM_OUT",\
            "TILT_FORWARD":"TILT_BACKWARD", "REVOLVE_CLOCKWISE":"REVOLVE_ANTICLOCKWISE",\
            "ROTATE_CLOCKWISE":"ROTATE_ANTICLOCKWISE"}

    for key, value in list(reverse_acts.iteritems()):
        reverse_acts[value] = key

    for col, range_ in ranges:
        print "\tcolumn ", col, " :"
        for value in range_:
            for act in acts[col]:
                try:
                    common = "last_op = '%s' AND %s = %d" % (act, col, value)
                    count_ = count(db, common)
                    prob =  prob_change(db, common)

                    #check probability of reverse
                    prob_rev =  probability(db, "next_op = '%s'" % reverse_acts[act], \
                            common + " AND duration > %d" % MIN_DURATION)

                    prob_reset_quit_ = prob_quit_reset(db, common)

                    if prob is not None and prob_rev is not None and prob_reset_quit_ is not None:
                        print "\t\t%-5d" % value, "%25s" % act, \
                          "total: %5d" % count_, \
                          "\tprob: %0.6f" % prob, \
                          "\tprob_rev: %0.6f" % prob_rev, \
                          "\tprob_r_q: %0.6f" % prob_reset_quit_
                except ZeroDivisionError:
                    pass
    
    print "The Selections During Change:"
    #To see how users change direction.
    for col, range_ in ranges:
        print "\tcolumn ", col, " :"
        for value in range_:
            print
            for act in (actions + ("QUIT", "RESET")):
                try: 
                    cond = "next_op = '%s'" % act
                    act1 = acts[col][0]
                    act2 = acts[col][1]
                    common = "%s = %d AND last_op <> next_op AND last_op <> '%s' " \
                              % (col, value, act1) + \
                             "AND last_op <> '%s' AND duration > %d" \
                              % (act2, MIN_DURATION)
                    count_ = count(db, common)
                    prob = probability(db, cond, common)
                    if prob is not None:
                        print "\t\t%-5d" % value, "%25s" % act, \
                            "total: %5d" % count_,\
                            "\tprob: %0.6f" % prob,\
                            "\tratio: %0.4f" % (prob / change_to_prob[act])
                except ZeroDivisionError:
                    pass





    


 


