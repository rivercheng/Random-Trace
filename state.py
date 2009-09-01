import sys

class State:
    dx = 0
    dy = 0
    dz = 0
    ax = 0
    ay = 0
    az = 0
    lastOp = None
    max_dx = 0
    max_dy = 0
    max_dz = 0
    min_dx = 0
    min_dy = 0
    min_dz = 0

    def __init__(self):
        pass

    def transition(self, operation):
        if operation is None:
            print >>sys.stderr, "unknown operation"
            sys.exit()
        elif operation == Ops.zoomIn:
            self.dz -= 1
            if self.dz < self.min_dz:
                self.min_dz = self.dz
        elif operation == Ops.zoomOut:
            self.dz += 1
            if self.dz > self.max_dz:
                self.max_dz = self.dz
        elif operation == Ops.moveLeft:
            self.dx -= 1
            if self.dx < self.min_dx:
                self.min_dx = self.dx
        elif operation == Ops.moveRight:
            self.dx += 1
            if self.dx > self.max_dx:
                self.max_dx = self.dx
        elif operation == Ops.moveUp:
            self.dy += 1
            if self.dy > self.max_dy:
                self.max_dy = self.dy
        elif operation == Ops.moveDown:
            self.dy -= 1
            if self.dy < self.min_dy:
                self.min_dy = self.dy
        elif operation == Ops.rotateXf:
            self.ax -= 10
            if (self.ax < 0):
                self.ax += 360
        elif operation == Ops.rotateXb:
            self.ax += 10
            if (self.ax >= 360):
                self.ax -= 360
        elif operation == Ops.rotateYleft:
            self.ay -= 10
            if (self.ay < 0):
                self.ay += 360
        elif operation == Ops.rotateYright:
            self.ay += 10
            if (self.ay >= 360):
                self.ay -= 360
        elif operation == Ops.rotateZclock:
            self.az += 10
            if (self.az >= 360):
                self.az -= 360
        elif operation == Ops.rotateZantiClock:
            self.az -= 10
            if (self.az < 0):
                self.az += 360
        elif operation == Ops.reset:
            self.reset()

        self.lastOp = operation

    def reset(self):
            self.dx = 0
            self.dy = 0
            self.dz = 15
            self.ax = 0
            self.ay = 0
            self.az = 0

    def init(self):
        self.reset()
        self.lastOp = Ops.unknown

    def toTuple(self):
        '''Convert state to the tuple representation'''
        return (self.dx, self.dy, self.dz, self.ax, self.ay, self.az, self.lastOp)

    def range(self):
        '''Output the bounding box'''
        return (self.min_dx, self.max_dx, self.min_dy, self.max_dy, self.min_dz, self.max_dz)








