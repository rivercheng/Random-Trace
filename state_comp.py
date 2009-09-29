'''Compare on those points who have enough samples'''

from __future__ import with_statement
import sqlite3
import sys
import cPickle
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
        #print act, prob
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

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage " + sys.argv[0] + "<db1 name> <db2 name> [threshold=20]"
        sys.exit()
    threshold = 20
    if len(sys.argv) > 3:
        threshold = int(sys.argv[3])

    conn = sqlite3.connect(sys.argv[1])
    db = "behavior"

    
    cols = ("x", "y", "z", "ax", "ay", "az")

    curr = query("DISTINCT x, y, z, ax, ay, az, last_op", db)
    stat = {}
    
    for item in curr:
        x, y, z, ax, ay, az, last_op = item
        c = query("next_op", db, "x = %d AND y = %d and z = %d and ax = %d and ay = %d and az = %d and last_op = '%s'" % item)
        dic = {}
        total = 0
        for i in c:
            dic[i[0]] = dic.get(i[0], 0) + 1
            total += 1
        if total < threshold:
            continue
        #print item, total
        for k in dic:
            dic[k] = dic[k] * 1.0 / total
        stat[(x,y,z,ax,ay,az,last_op)] = dic

    stat2 = {}
    conn = sqlite3.connect(sys.argv[2])
    for state in stat:
        curr = query("next_op", db, "x = %d AND y = %d AND z = %d AND ax = %d AND ay = %d and az = %d and last_op = '%s'" % state)
        dic = {}
        stat2[state] = dic
        total = 0
        for op in curr:
            dic[op[0]] = dic.get(op[0],  0) + 1
            total += 1
        if total > 0:
            for k in dic:
                dic[k] = dic[k] * 1.0 / total

    for s in stat:
        print s
        for op in stat[s]:
            res = stat2[s].get(op, 0)
            print op, stat[s][op], res, abs(res - stat[s][op])



    







    



    
    

    





    


 


