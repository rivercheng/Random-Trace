'''Read Trace file, and convert it to records for analysing.'''
from __future__ import with_statement
import os
import sys
import sqlite3
def parse_line(line):
    '''Parse a line to time and operation
    
    The format of a line is :'Sec Microsec Operation'.
    If Operation is BEGIN, the time is the absolute time,
    else the time the relative time of the operation to the begin time.
    '''
    entries = line.split()

    #ignore a line with more than 3 items.
    if len(entries) < 3:
        return None
    try:
        sec = int(entries[0])
        microsec = int(entries[1])
        op = entries[2]
        return (sec*1000000 + microsec, op)
    except:
        #ignore any error lines
        return None

def parse_files(path):
    '''parse the behavior files in a directory to (op, duration) tuples.'''
    for name in os.listdir(path):
        #ignore none "behavior" files
        if "behavior" not in name:
            continue
        fullname = os.path.join(path, name)
        with open(fullname, "r") as f:
            prev_ops = None
            prev_time = 0
            for line in f:
                res = parse_line(line)
                if not res: 
                    continue
                time_, ops = res
                #if ops is BEGIN, 
                #the time is the absolute time, which can be ignored.
                if ops == "BEGIN": 
                    prev_ops = ops
                    prev_time = 0
                else:
                    prev_duration = time_ - prev_time
                    
                    #throw away all the rest traces when MOUSE action exists
                    if "MOUSE" in ops:
                        yield prev_ops, prev_duration
                        prev_ops = None
                        break
                    else:
                        yield prev_ops, prev_duration
                        prev_ops = ops
                        prev_time = time_
            if prev_ops != "QUIT" and prev_ops is not None:
                yield prev_ops, 200000

def create_transformer(dict1 = None):
    '''create two closures. 
    
    One converts each operation to an index and the other do the reverse.'''
    if dict1 is None:
        dict1 = {}
    dict2 = {}
    for key, value in dict1.iteritems():
        dict2[value] = key
    def transformer(operation):
        '''convert operation to index'''
        if operation in dict1:
            return dict1[operation]
        else:
            i = len(dict1)
            dict1[operation] = i
            dict2[i] = operation
            return i
    def rev_transformer(index):
        '''convert index to operation'''
        return dict2[index]
    return transformer, rev_transformer

class State:
    '''Store the state of current view point'''
    def __init__(self, state=None):
        ''' initate current state from previous state.'''
        if state is None:
            self.x = 0
            self.y = 0
            self.z = 0
            self.ax = 0
            self.az = 0
            self.ay = 0
            self.az = 0
            self.last_last_op = None
            self.last_op = None
            self.next_op = "END"
            self.count = 0
            self.duration = 0
        else:
            self.x = state.x
            self.y = state.y
            self.z = state.z
            self.ax = state.ax
            self.ay = state.ay
            self.az = state.az
            self.last_last_op = state.last_op
            self.last_op = state.next_op
            self.next_op = None
            self.count = state.count
            self.duration = 0
    def __repr__(self):
        '''to enable printing this class.'''
        return str((self.x, self.y, self.z, self.ax, self.ay, self.az, \
                self.last_op, self.next_op, self.count, self.duration))

def transit(operation, duration, last_state):
    '''Transition from one state to another state,
       according to the given operation.'''
    if (operation != "BEGIN"):
        last_state.next_op = operation
    else:
        last_state.next_op = "QUIT"
    state = State(last_state)
    state.duration = duration
    if operation == last_state.last_op:
        state.count += 1
    else:
        state.count = 0
    if operation == "ZOOM_IN":
        state.z += 1
    elif operation == "ZOOM_OUT":
        state.z -= 1
    elif operation == "MOVE_LEFT":
        state.x -= 1
    elif operation == "MOVE_RIGHT":
        state.x += 1
    elif operation == "MOVE_UP":
        state.y += 1
    elif operation == "MOVE_DOWN":
        state.y -= 1
    elif operation == "TILT_FORWARD":
        state.ax -= 1
        state.ax %= 36
    elif operation == "TILT_BACKWARD":
        state.ax += 1
        state.ax %= 36
    elif operation == "REVOLVE_CLOCKWISE":
        state.ay -= 1
        state.ay %= 36
    elif operation == "REVOLVE_ANTICLOCKWISE":
        state.ay += 1
        state.ay %= 36
    elif operation == "ROTATE_CLOCKWISE":
        state.az += 1
        state.az %= 36
    elif operation == "ROTATE_ANTICLOCKWISE":
        state.az -= 1
        state.az %= 36
    elif operation == "BEGIN":
        state = State()
        state.duration = duration
        state.last_op = "BEGIN"
    elif operation == "RESET":
        state = State()
        state.duration = duration
        state.last_op = "RESET"
    elif operation == "QUIT":
        state = State()
        state.duration = duration
        state.last_op = "QUIT"
    else:
        print "Unknown operation ", operation
        sys.exit(1)
    return state

def output_state(state, op2id, conn):
    '''output the state'''
    if state.last_op is not None:
        tup = (state.x, state.y, state.z, state.ax, state.ay, state.az,\
            op2id(state.last_op), op2id(state.next_op), state.count, state.duration,\
            state.last_last_op, state.last_op, state.next_op)
        #print "%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%12d\t%30s\t%30s" % tup
        conn.execute("insert into behavior values \
                     (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tup)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: " + sys.argv[0] + " <path> <db name>"
        sys.exit()
    opt_id, id_opt = create_transformer()
    prev_state = State()

    os.system("rm "+sys.argv[2])
    
    conn = sqlite3.connect(sys.argv[2])
    
    db = "behavior"
    cols = ("x", "y", "z", "ax", "ay", "az", "duration", "last_op", "next_op")
    actions = ("ZOOM_IN", "ZOOM_OUT", "MOVE_LEFT", "MOVE_RIGHT", "MOVE_UP", "MOVE_DOWN", \
               "TILT_FORWARD", "TILT_BACKWARD", "REVOLVE_CLOCKWISE", "REVOLVE_ANTICLOCKWISE",\
               "ROTATE_CLOCKWISE", "ROTATE_ANTICLOCKWISE")

    conn.execute("create table "+ db + \
        "(x integer, y integer, z integer, \
         ax integer, ay integer, az integer, \
         last_op_index integer, next_op_index integer, \
         count integer, duration integer, \
         last_last_op text,\
         last_op text, next_op text)")

    for opt, time in parse_files(sys.argv[1]):
        curr_state = transit(opt, time, prev_state)
        output_state(prev_state, opt_id, conn)
        prev_state = curr_state

    for col in cols:
        conn.execute("CREATE INDEX "+ col + " ON " + db + \
                "(%s)" % col)
    conn.execute("CREATE INDEX cood ON " + db + "(x, y, z, ax, ay, az)")

