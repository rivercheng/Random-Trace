from __future__ import with_statement
import sqlite3
import sys
import cPickle
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

def outputBeginProbability(actions, db, f):
    beginDict = {}
    print "The begin probability:"
    for act in actions:
        prob =  probability(db, "next_op = '%s'" % act, \
                "next_op <> 'QUIT' AND (last_op = 'RESET' OR last_op = 'BEGIN')") 
        print act, prob
        beginDict[act] = prob
    print
    cPickle.dump(beginDict, f)


def outputPopularity(ranges, db, f):
    popularityDict = {}
    print "Popularity:"
    for col, range_ in ranges:
        print "\tcolumn ", col, " :"
        popularityDict[col] = {}
        for value in range_:
            prob = popularity(db, "%s=%d" % (col, value))
            print "\t\t%-10d" % value, "%0.6f" % prob
            popularityDict[col][value] = prob
    print 
    cPickle.dump(popularityDict, f)

def outputContinueProbability(ranges, reverse_acts, db, f):
    continueDict = {}
    MIN_COUNT = 10
    print "Change Probability:"
    for col, range_ in ranges:
        print "\tcolumn ", col, " :"
        continueDict[col] = {}
        for value in range_:
            continueDict[col][value] = {}
            for act in acts[col]:
                continueDict[col][value][act] = None
                try:
                    common = "last_op = '%s' AND %s = %d" % (act, col, value)
                    count_ = count(db, common)
                    prob =  prob_change(db, common)
                    #check probability of reverse
                    prob_rev =  probability(db, "next_op = '%s'" % reverse_acts[act], \
                            common + " AND duration > %d" % MIN_DURATION)
                    prob_reset_quit_ = prob_quit_reset(db, common)
                    if prob is not None and prob_rev is not None and prob_reset_quit_ is not None:
                        continueDict[col][value][act] = (count_, 1 - prob, prob_rev, prob_reset_quit_)
                except ZeroDivisionError:
                    pass

        for value in range_:
            for act in acts[col]:
                if continueDict[col][value][act] is None:
                    #default go to zero
                    if value < 0:
                        if act == acts[col][0]:
                            continueDict[col][value][act] = (0, 0, 1, 0)
                        else:
                            continueDict[col][value][act] = (0, 1, 0, 0)
                    else:
                        if act == acts[col][0]:
                            continueDict[col][value][act] = (0, 1, 0, 0)
                        else:
                            continueDict[col][value][act] = (0, 0, 1, 0)
                        
                count_, prob_con, prob_rev, prob_reset_quit_ = continueDict[col][value][act]
                print "\t\t%-5d" % value, "%25s" % act, \
                          "total: %5d" % count_, \
                          "\tprob: %0.6f" % prob_con, \
                          "\tprob_rev: %0.6f" % prob_rev, \
                          "\tprob_r_q: %0.6f" % prob_reset_quit_
                #continueDict[col][value][act] = (prob_con, prob_rev)
    cPickle.dump(continueDict, f)

def outputThinktime(f_cont, f_change, f):
    continue_think_time_lst = []
    change_think_time_lst   = []
    for line in open(f_cont):
        continue_think_time_lst.append(int(line))
    for line in open(f_change):
        change_think_time_lst.append(int(line))
    cPickle.dump(continue_think_time_lst, f)
    cPickle.dump(change_think_time_lst, f)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage " + sys.argv[0] + "<db name>"
        sys.exit()
    conn = sqlite3.connect(sys.argv[1])
    db = "behavior"
    
    cols = ("x", "y", "z", "ax", "ay", "az")
    other_cols = ("duration", )
    actions = ("ZOOM_IN", "ZOOM_OUT", "MOVE_LEFT", "MOVE_RIGHT", "MOVE_UP", "MOVE_DOWN", \
               "TILT_FORWARD", "TILT_BACKWARD", "REVOLVE_CLOCKWISE", "REVOLVE_ANTICLOCKWISE",\
               "ROTATE_CLOCKWISE", "ROTATE_ANTICLOCKWISE")
    
    ranges = []
    for col in cols:
        ranges.append( (col, range(db, col)) )
    
    acts = {"x": ("MOVE_LEFT", "MOVE_RIGHT"), "y" : ("MOVE_DOWN", "MOVE_UP"), \
            "z" : ("ZOOM_OUT", "ZOOM_IN"), "ax": ("TILT_FORWARD", "TILT_BACKWARD"), \
            "ay": ("REVOLVE_CLOCKWISE", "REVOLVE_ANTICLOCKWISE"), \
            "az": ("ROTATE_ANTICLOCKWISE", "ROTATE_CLOCKWISE")}

    reverse_acts = {"MOVE_LEFT" : "MOVE_RIGHT", "MOVE_UP":"MOVE_DOWN", "ZOOM_IN":"ZOOM_OUT",\
            "TILT_FORWARD":"TILT_BACKWARD", "REVOLVE_CLOCKWISE":"REVOLVE_ANTICLOCKWISE",\
            "ROTATE_CLOCKWISE":"ROTATE_ANTICLOCKWISE"}

    for key, value in list(reverse_acts.iteritems()):
        reverse_acts[value] = key
    
    with open(sys.argv[1]+".pickle", 'w') as out_file:
        outputBeginProbability(actions, db, out_file)
        outputPopularity(ranges, db, out_file)
        outputContinueProbability(ranges, reverse_acts, db, out_file)
        outputThinktime("continue_think_time", "change_think_time", out_file)

    print "General Probability of Actions:"
    general_prob = {}
    for action in (actions + ("QUIT", "RESET")):
        prob =  probability(db, "next_op = '%s'" % action, None)
        general_prob[action] = prob
        if prob is not None:
            print "%30s" % action, ": ", "%0.4f" % prob
    print

    print "Continue and Reverse Probability"
    total_count = 0;
    continue_count = 0;
    reverse_count = 0;
    for action in actions:
        total_count += count(db, "last_op == '%s'"%action)
        continue_count += count(db, "last_op == '%s' AND next_op == '%s'"%(action, action))
        reverse_count += count(db, "last_op == '%s' AND next_op == '%s'"%(action, reverse_acts[action]))
    print total_count, continue_count, reverse_count, total_count - continue_count - reverse_count
    print 1 , continue_count * 1.0 / total_count, reverse_count * 1.0 / total_count, (total_count - continue_count - reverse_count) * 1.0 / total_count



    print "Change Probability:"
    print "%30s" % "General", ": ", "%0.4f" % probability(db, "next_op <> last_op", None)
    for action in actions:
        prob = probability(db, "next_op != last_op", "last_op = '%s'" % action)
        if prob is not None:
            print "%30s" % action, ": ", "%0.4f" % prob, "%0.4f" % (1 - prob)
    

    

    print "Considering two previous actions"
    cursor = query("last_last_op, last_op, next_op", db)
    m = {}
    for res in cursor:
        last_last_op, last_op, next_op = res
        if (last_last_op, last_op) in m:
            m[(last_last_op, last_op)]["total"] = m[(last_last_op, last_op)].get("total", 0) + 1
            m[(last_last_op, last_op)][next_op] = m[(last_last_op, last_op)].get(next_op, 0) + 1
        else:
            m[(last_last_op, last_op)] = {}
    total = 0
    first = 0
    second = 0
    for k,v in m.iteritems():
        count_array = []
        for k2, v2 in v.iteritems():
            count_array.append(v2)
        count_array.sort(reverse=True)
        if count_array:
            total += count_array[0]
            first += count_array[1]
        if len(count_array) > 2:
            second += count_array[2]
    print total, first, first+second, first * 1.0 / total, (first+second) * 1.0 /total











    


 


