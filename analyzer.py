from __future__ import with_statement
import sqlite3
import sys
import readline
conn = sqlite3.connect(":memory:")
conn.execute("create table behavior \
        (x integer, y integer, z integer, \
         ax integer, ay integer, az integer, \
         last_op_index integer, next_op_index integer, \
         count integer, duration integer, \
         last_op text, next_op text)")
with open('res', 'r') as f_input:
    for line in f_input:
        tup = line.split()
        conn.execute("insert into behavior values \
                     (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tup)

while(True):
    try:
        str = raw_input(">")
        if str == "": sys.exit(0)
    except EOFError:
        sys.exit(0)
    try:
        c = conn.execute(str)
        for row in c:
            for entry in row:
                print entry,
            print
    except sqlite3.Error, err:
        print err.args[0]



 


