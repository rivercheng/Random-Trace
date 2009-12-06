from __future__ import with_statement
import sqlite3
import sys
import cPickle
import pylab
import numpy as np
MIN_DURATION = 0

def query(column, db, condition=None):
    query_str = "SELECT "+column+" FROM "+db
    if (condition is not None):
        query_str += " WHERE "+condition
    #print query_str
    return  conn.execute(query_str)

def most_frequent(occurence_map):
    lst = []
    for action, count in occurence_map.iteritems():
        lst.append((count, action))
    lst.sort(reverse=True)
    return lst[1]

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

def autolabel(ax, rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 
                    1.01*height, '%0.3f'%height,
                    ha='center', va='bottom')

def plot_bar_graph(lst1, lst2, lst3, lst4):
    ind = np.arange(3)
    width = 0.2
    meshes = ['Buddha', 'Dragon', 'Thai']
    methods = ['None', 'Action', 'Vp', 'Vp+Action']
    
    pylab.bar(ind, lst1, width, facecolor='none', hatch='//', label=methods[0])
    pylab.bar(ind+width, lst2, width, facecolor='none', hatch='--', label=methods[1])
    pylab.bar(ind+2*width, lst3, width, facecolor='none', hatch='\\\\', label=methods[2])
    pylab.bar(ind+3*width, lst4, width, facecolor='none', hatch='xx', label=methods[3])
    pylab.ylim(0, 1)
    pylab.ylabel('Accuracy of Prediction')
    pylab.xlabel('Mesh')
    pylab.title('Comparison of Four Prediction Methods')
    pylab.xticks(ind+2*width, meshes)
    pylab.legend(loc='lower right')

    #label
    for i in range(3):
        pylab.text(i+0.5*width, lst1[i]*1.01, "%0.3f"%lst1[i], ha='center', va='bottom', fontsize='small')
        pylab.text(i+1.5*width, lst2[i]*1.01, "%0.3f"%lst2[i], ha='center', va='bottom', fontsize='small')
        pylab.text(i+2.5*width, lst3[i]*1.01, "%0.3f"%lst3[i], ha='center', va='bottom', fontsize='small')
        pylab.text(i+3.5*width, lst4[i]*1.01, "%0.3f"%lst4[i], ha='center', va='bottom', fontsize='small')

if __name__ == "__main__":
  files = ["happy.db", "dragon.db", "huge.db"]
  names = ["Buddha", "Dragon", "Thai"]
  accuracy_list_global = []
  accuracy_list_cont = []
  accuracy_list_vp = []
  accuracy_list_state = []
  for f, name in zip(files, names):
    conn = sqlite3.connect(f)
    db = "behavior"
    
    Threshold = 10

    cursor = query("x, y, z, ax, ay, az, last_op, next_op", db)
    m_vp = {}
    m_state = {}
    for res in cursor:
        x, y, z, ax, ay, az = map(int, res[:6])
        last_op, next_op = res[6:]
        if (x,y,z,ax,ay,az) not in m_vp:
            m_vp[(x,y,z,ax,ay,az)] = {}
            m_vp[(x,y,z,ax,ay,az)]["total"] = 0
        if (x,y,z,ax,ay,az,last_op) not in m_state:
            m_state[(x,y,z,ax,ay,az,last_op)] = {}
            m_state[(x,y,z,ax,ay,az,last_op)]["total"] = 0

        m_vp[(x,y,z,ax,ay,az)]["total"] += 1
        m_vp[(x,y,z,ax,ay,az)][next_op] = m_vp[(x,y,z,ax,ay,az)].get(next_op, 0) + 1
        m_state[(x,y,z,ax,ay,az,last_op)][next_op] = m_state[(x,y,z,ax,ay,az,last_op)].get(next_op, 0) + 1
        m_state[(x,y,z,ax,ay,az,last_op)]["total"] += 1

    total = 0
    correct = 0
    for vp, occurence_map in m_vp.iteritems():
        total_count = occurence_map["total"] 
        if total_count > Threshold:
            total += total_count
            max_count, s = most_frequent(occurence_map)
            correct += max_count

    print total, correct, float(correct)/total
    accuracy_vp = float(correct) / total


    total = 0
    correct = 0
    for vp, occurence_map in m_state.iteritems():
        total_count = occurence_map["total"] 
        if total_count > Threshold:
            total += total_count
            max_count, s = most_frequent(occurence_map)
            correct += max_count

    print total, correct, float(correct)/total
    accuracy_state = float(correct) / total
    
    accuracy_continue = prob_continue(db)
    

    actions = ("ZOOM_IN", "ZOOM_OUT", "MOVE_LEFT", "MOVE_RIGHT", "MOVE_UP", "MOVE_DOWN", \
               "TILT_FORWARD", "TILT_BACKWARD", "REVOLVE_CLOCKWISE", "REVOLVE_ANTICLOCKWISE",\
               "ROTATE_CLOCKWISE", "ROTATE_ANTICLOCKWISE")

    max_prob = 0
    for action in actions:
        prob = probability(db, "next_op = '%s'"%action, None)
        if prob > max_prob: max_prob = prob
    accuracy_global = max_prob

    accuracy_list_global.append(accuracy_global)
    accuracy_list_cont.append(accuracy_continue)
    accuracy_list_vp.append(accuracy_vp)
    accuracy_list_state.append(accuracy_state)

  plot_bar_graph(accuracy_list_global, accuracy_list_cont, accuracy_list_vp, accuracy_list_state)
  pylab.savefig('accuracy_comp.eps')










    


 


