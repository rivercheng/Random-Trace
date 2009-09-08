'''Read Trace file, and convert it to records for analysing.'''
from __future__ import with_statement
import os
import sys
import sqlite3
import extend_random

def divide_files(path, path_o1, path_o2):
    '''randomly divide files in a directory to two directories.'''
    for name in os.listdir(path):
        #ignore none "behavior" files
        if "behavior" not in name:
            continue
        fullname = os.path.join(path, name)
        rand = extend_random.nextDouble()
        if rand < 0.5:
            output_fullname = os.path.join(path_o1, name)
        else:
            output_fullname = os.path.join(path_o2, name)
        os.system("mkdir -p "+path_o1)
        os.system("mkdir -p "+path_o2)
        os.system("cp -f %s %s" % (fullname, output_fullname))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Usage: " + sys.argv[0] + " <path> <output path 1> <output path 2>"
        sys.exit()

    extend_random.set_seed(1)
    divide_files(sys.argv[1], sys.argv[2], sys.argv[3])

