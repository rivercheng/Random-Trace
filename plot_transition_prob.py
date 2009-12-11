from __future__ import with_statement
import sqlite3
import sys
import matplotlib.pyplot as plt
import numpy as np
from correlation import correlation
MIN_DURATION = 0
actions = ( "MOVE_LEFT", "MOVE_RIGHT", "MOVE_UP", "MOVE_DOWN", "ZOOM_IN", "ZOOM_OUT",
            "TILT_FORWARD", "TILT_BACKWARD", "REVOLVE_CLOCKWISE", "REVOLVE_ANTICLOCKWISE",
            "ROTATE_CLOCKWISE", "ROTATE_ANTICLOCKWISE")

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

def prob_continue(db, condition = None):
    if condition is not None:
        return probability(db, "last_op = next_op", "%s and duration > %d" % (condition, MIN_DURATION))
    else:
        return probability(db, "last_op = next_op", "duration > %d" % MIN_DURATION)

def stat(cursor):
    m_g = {}
    for res in cursor:
        next_op = res[0]
        m_g["total"] = m_g.get("total", 0) + 1
        m_g[next_op] = m_g.get(next_op, 0) + 1
    return m_g

def autolabel(ax, rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 
                    1.01*height, '%0.3f'%height,
                    ha='center', va='bottom')

def plot_transition(state, m_general_1, m_general_2, output_name):
    prob_general_1 = []
    prob_general_2 = []
    for action in actions:
        prob_general_1.append(m_general_1.get(action, 0) * 1.0 / m_general_1["total"])
        prob_general_2.append(m_general_2.get(action, 0) * 1.0 / m_general_2["total"])
    
    ind = np.arange(len(actions))
    width = 0.35
    names = ["ML", "MR", "MU", "MD", "ZI", "ZO", "TF", "TB", "REC", "REAN", "ROC", "ROAN"]

    fig = plt.figure()
    axis  = fig.add_subplot(111)
    rect1 = axis.bar(ind, prob_general_1, width, facecolor = 'none', hatch = '//', label="Real")
    rect2 = axis.bar(ind+width, prob_general_2, width, facecolor='none', hatch='\\\\', label="Synthetic")
    x, y, z, ax, ay, az, last_op = state


    axis.axis(ymin=0, ymax=1)
    axis.set_ylabel('Probability of Action')
    axis.set_xlabel('Action')
    axis.set_title('x=%s, y=%s, z=%s, ax=%s, ay=%s, az=%s, A_p=%s, count: %d'%(x,y,z,ax,ay,az,last_op, m_general_1["total"]))
    axis.set_xticks(ind+width)
    axis.set_xticklabels(names, fontsize='small')
    axis.legend(loc="upper left")
    axis.text(5, 0.95, "correlation: %0.3f"%correlation(prob_general_1, prob_general_2), horizontalalignment='center')
    #autolabel(ax, rect1)
    #autolabel(ax, rect2)
    plt.savefig(output_name)
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Usage: ", sys.argv[0], "<db1> <db2> <threshold>"
        sys.exit()

    threshold = int(sys.argv[3])

    #find out the most frequent states
    conn = sqlite3.connect(sys.argv[1])
    db = "behavior"
    m = {}
    m["total"] = 0
    cursor = query("x,y,z,ax,ay,az,last_op", db)
    for res in cursor:
        x,y,z,ax,ay,az,last_op = res
        if last_op in actions:
            m["total"] += 1
            m[(x,y,z,ax,ay,az,last_op)] = m.get((x,y,z,ax,ay,az,last_op), 0) + 1

    lst=[]
    for state in m:
        if state == "total": continue
        lst.append((m[state], state))
    lst.sort(reverse=True)

    states = []
    for c, state in lst:
        if c < threshold : break
        print state
        states.append(state)

    seq_no = 1
    for state in states:
        conn = sqlite3.connect(sys.argv[1])
        db = "behavior"
        cursor = query("next_op", db, "x=%s AND y=%s AND z=%s AND ax=%s AND ay=%s AND az=%s AND last_op='%s'"%state)
        m_general_1 = stat(cursor)

        conn = sqlite3.connect(sys.argv[2])
        db = "behavior"
        cursor = query("next_op", db, "x=%s AND y=%s AND z=%s AND ax=%s AND ay=%s AND az=%s AND last_op='%s'"%state)
        m_general_2 = stat(cursor)

        plot_transition(state, m_general_1, m_general_2, "transition"+str(seq_no)+".eps")
        seq_no += 1







