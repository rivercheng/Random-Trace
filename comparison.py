from __future__ import with_statement
import sqlite3
import sys
import matplotlib.pyplot as plt
import numpy as np
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
    
    m = {}
    m_c = {}
    m_g = {}
    for action in actions:
        m_c[action] = {}
    for res in cursor:
        last_op, next_op = res
        
        m_g["total"] = m_g.get("total", 0) + 1
        m_g[next_op] = m_g.get(next_op, 0) + 1

        m["total"] = m.get("total", 0) + 1
        if last_op == next_op:
            m["continue"] = m.get("continue", 0) + 1
            m[last_op] = m.get(last_op, 0) + 1

        if last_op not in actions:
            continue
        m_c[last_op][next_op] = m_c[last_op].get(next_op, 0) + 1
        m_c[last_op]["total"] = m_c[last_op].get("total", 0) + 1
    return m, m_c, m_g

def autolabel(ax, rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 
                    1.01*height, '%0.3f'%height,
                    ha='center', va='bottom')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: ", sys.argv[0], "<db1> <db2>"
        sys.exit()

    conn = sqlite3.connect(sys.argv[1])
    db = "behavior"
    cursor = query("last_op, next_op", db)
    m_continue_1, m_relation_1, m_general_1 = stat(cursor)

    conn = sqlite3.connect(sys.argv[2])
    db = "behavior"
    cursor2 = query("last_op, next_op", db)
    m_continue_2, m_relation_2, m_general_2 = stat(cursor2)

    #draw general probability
    prob_general_1 = []
    prob_general_2 = []
    for action in actions:
        prob_general_1.append(m_general_1[action] * 1.0 / m_general_1["total"])
        prob_general_2.append(m_general_2[action] * 1.0 / m_general_2["total"])


    ind = np.arange(len(actions))
    width = 0.35
    names = ["ML", "MR", "MU", "MD", "ZI", "ZO", "TF", "TB", "REC", "REAN", "ROC", "ROAN"]

    fig = plt.figure()
    ax  = fig.add_subplot(111)
    rect1 = ax.bar(ind, prob_general_1, width, facecolor = 'none', hatch = '//', label="Real")
    rect2 = ax.bar(ind+width, prob_general_2, width, facecolor='none', hatch='\\\\', label="Synthetic")
    ax.axis(ymin=0, ymax=0.5)
    ax.set_ylabel('Probability of Action')
    ax.set_ylabel('Action')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(names, fontsize='small')
    ax.legend(loc="upper right")
    #autolabel(ax, rect1)
    #autolabel(ax, rect2)
    plt.savefig("general_prob_comp.eps")
    plt.close()

    prob_continue_1 = []
    prob_continue_2 = []
    prob_continue_1.append(m_continue_1["continue"] * 1.0 / m_continue_1["total"])
    prob_continue_2.append(m_continue_2["continue"] * 1.0 / m_continue_2["total"])
    for action in actions:
        prob_continue_1.append(m_continue_1[action] * 1.0 / m_general_1[action])
        prob_continue_2.append(m_continue_2[action] * 1.0 / m_general_2[action])
    
    ind = np.arange(len(actions)+1)
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    rect1 = ax.bar(ind, prob_continue_1, width, facecolor = 'none', hatch = '//', label="Real")
    rect2 = ax.bar(ind+width, prob_continue_2, width, facecolor='none', hatch='\\\\', label="Synthetic")
    ax.axis(ymin=0, ymax=1)
    ax.set_ylabel('Probability of Action')
    ax.set_ylabel('Action')
    ax.set_xticks(ind+width)
    names = ["General"] + names
    ax.set_xticklabels(names, fontsize='small')
    ax.legend(loc="upper right")
    #autolabel(ax, rect1)
    #autolabel(ax, rect2)
    plt.savefig("continue_prob_comp.eps")


