from __future__ import with_statement
import sqlite3
import sys
import cPickle
import pylab
MIN_DURATION = 20000

def query(column, db, condition=None):
    query_str = "SELECT "+column+" FROM "+db
    if (condition is not None):
        query_str += " WHERE "+condition
    #print query_str
    return  conn.execute(query_str)

def CDF_lst(lst, count):
    cdf_lst = []
    length = len(lst)
    for i in range(count):
        index = length * i / count
        cdf_lst.append(lst[index])
    cdf_lst.append(lst[-1])
    return cdf_lst

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage " + sys.argv[0] + "<db name> <output file>"
        sys.exit()
    conn = sqlite3.connect(sys.argv[1])
    db = "behavior"
    
    cursor = query("last_op, next_op, duration", db, "duration > %d AND next_op <> 'QUIT' AND last_op <> 'BEGIN'"%MIN_DURATION)
    general_duration = []
    continue_duration = []
    change_duration = []
    for res in cursor:
        last_op, next_op, duration = res
        duration = float(duration)/1000000
        general_duration.append(duration)
        if last_op == next_op:
            continue_duration.append(duration)
        else:
            change_duration.append(duration)

    general_duration.sort()
    continue_duration.sort()
    change_duration.sort()

    f_continue = open("continue_think_time", "w")
    f_change =   open("change_think_time", "w")
    for t in continue_duration:
        print >>f_continue, t
    for t in change_duration:
        print >>f_change, t

    #plot CDF
    general_cdf = CDF_lst(general_duration, 100)
    continue_cdf = CDF_lst(continue_duration, 100)
    change_cdf   = CDF_lst(change_duration, 100)
    y_lst = [y / 100.0 for y in range(101)]
    

    pylab.semilogx(general_cdf, y_lst, 'k-', label="General", )
    pylab.semilogx(continue_cdf, y_lst, 'b--', label="Continue")
    pylab.semilogx(change_cdf, y_lst, 'r-.', label="Change")
    pylab.legend(loc='lower right')
    pylab.xlim(0,100)
    pylab.xlabel('time(s)')
    pylab.ylabel('CDF')
    pylab.yticks([y / 10.0 for y in range(11)])
    pylab.savefig(sys.argv[2])










    


 


