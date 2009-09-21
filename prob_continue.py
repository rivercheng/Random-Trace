from __future__ import with_statement
import sqlite3
import sys
import cPickle
import math
import analyze

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
    changeDict = {}
    print "Change Probability:"
    for col, range_ in ranges:
        print "\tcolumn ", col, " :"
        changeDict[col] = {}
        for value in range_:
            changeDict[col][value] = {}
            for act in acts[col]:
                #by default, the next action is to reverse.
                changeDict[col][value][act] = (0, 1)
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
                        changeDict[col][value][act] = (1-prob, prob_rev)
                except ZeroDivisionError:
                    pass
    cPickle.dump(changeDict, f)

def obtainPopularity(ranges, db):
    popularityDict = {}
    print "Popularity:"
    for col, range_ in ranges:
        popularityDict[col] = {}
        for value in range_:
            prob = popularity(db, "%s=%d" % (col, value))
            popularityDict[col][value] = prob
    return popularityDict

def probToIndex(prob):
    i = int(round(math.log(prob, 10)))
    return -i

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage " + sys.argv[0] + "<db name>"
        sys.exit()
    number = None
    if len(sys.argv) > 2:
        number = int(sys.argv[2])

    conn = sqlite3.connect(sys.argv[1])
    db = "behavior"
    
    cols = ("x", "y", "z", "ax", "ay", "az")

    curr = query("x, y, z, ax, ay, az, last_op, next_op", db, "duration > 20000 AND last_op != 'BEGIN'")
    dist = []
    sum  = 0
    
    reverse_acts = {"MOVE_LEFT" : "MOVE_RIGHT", "MOVE_UP":"MOVE_DOWN", "ZOOM_IN":"ZOOM_OUT",\
            "TILT_FORWARD":"TILT_BACKWARD", "REVOLVE_CLOCKWISE":"REVOLVE_ANTICLOCKWISE",\
            "ROTATE_CLOCKWISE":"ROTATE_ANTICLOCKWISE"}

    
    for key, value in list(reverse_acts.iteritems()):
        reverse_acts[value] = key
    
    ranges = []
    for col in cols:
        ranges.append( (col, range(db, col)) )
    
    popularityDict = obtainPopularity(ranges, db)

    count_dict = {}
    
    for item in curr:
        x, y, z, ax, ay, az, last_op, next_op = item
        prob = popularityDict["x"][x] * popularityDict["y"][y] * popularityDict["z"][z]\
               *popularityDict["ax"][ax] * popularityDict["ay"][ay] * popularityDict["az"][az]
        dict_p = count_dict.get(probToIndex(prob), {})
        count_dict[probToIndex(prob)] = dict_p
        dict_p["total"] = dict_p.get("total", 0) + 1
        try:
            if last_op == next_op:
                action = "continue"
                dict_p["continue"] = dict_p.get("continue", 0) + 1
            elif last_op == reverse_acts[next_op]:
                action = "reverse"
                dict_p["reverse"] = dict_p.get("reverse", 0) + 1
            else:
                action = "change"
                dict_p["change"] = dict_p.get("change", 0) + 1
        except KeyError:
            action = "change"
            dict_p["change"] = dict_p.get("change", 0) + 1
        #print prob, action, x, y, z, ax, ay, az, last_op, next_op

    for i in count_dict:
        for action in count_dict[i]:
            print i, action, count_dict[i][action], count_dict[i][action] * 1.0 /count_dict[i]["total"]






    



    
    

    





    


 


