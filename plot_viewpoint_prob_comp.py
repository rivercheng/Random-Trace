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

def output_res_lst():
    cursor = query("x, y, z, ax, ay, az", db)
    m = {}
    m["total"] = 0
    for res in cursor:
        x,y,z,ax,ay,az = res
        m[(x,y,z,ax,ay,az)] = m.get((x,y,z,ax,ay,az), 0) + 1
        m["total"] += 1
    return m

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage " + sys.argv[0] + "<db1 name> <db2 name> [count]"
        sys.exit()
    conn = sqlite3.connect(sys.argv[1])
    db = "behavior"

    m1 = output_res_lst()
    res_lst_1 = []
    for vp in m1:
        if vp == "total": continue
        res_lst_1.append((m1[vp]*1.0/m1["total"], vp))
    res_lst_1.sort(reverse=True)
    if [sys.argv] < 4:
        n = len(res_lst_1)
    else:
        n = int(sys.argv[3])


    conn = sqlite3.connect(sys.argv[2])
    m2 = output_res_lst()

    res_lst_2 = []
    i = 0
    for count, vp in res_lst_1:
        if i >= n: break
        i += 1
        res_lst_2.append(m2.get(vp, 0)*1.0/m2["total"])

    res_lst_1 = [count for count, vp in res_lst_1[:n]]

    pylab.plot(res_lst_1)
    pylab.plot(res_lst_2)
    pylab.show()



    


        







    


 


