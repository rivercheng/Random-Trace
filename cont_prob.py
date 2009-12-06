from __future__ import with_statement
import sqlite3
import sys
MIN_DURATION = 0

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

if __name__ == "__main__":
    files = ['happyN.db', 'happyD1.db', 'happyD2.db',
             'dragonN.db', 'dragonD1.db', 'dragonD2.db',
             'hugeN.db', 'hugeD1.db', 'hugeD2.db']
    names = ['Happy', 'HappyD1', 'HappyD2',
             'Dragon', 'DragonD1', 'DragonD2',
             'Thai', 'ThaiD1', 'ThaiD2']
    for i in range(9):
        conn = sqlite3.connect(files[i])
        db = "behavior"
        print names[i], prob_continue(db)
