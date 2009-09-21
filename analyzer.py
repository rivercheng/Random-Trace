from __future__ import with_statement
import sqlite3
import sys
import readline
if len(sys.argv) < 2:
    print "Usage ", sys.argv[0], "<db name>"
    sys.exit(1)

conn = sqlite3.connect(sys.argv[1])

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



 


