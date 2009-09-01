
class Ops:
    unknown = "unknown"
    zoomIn  = "ZI" 
    zoomOut = "ZO"
    moveLeft = "ML"
    moveRight = "MR"
    moveUp   = "MU"
    moveDown = "MD"
    rotateXf = "RXF"
    rotateXb = "RXB"
    rotateYleft = "RYL"
    rotateYright = "RYR"
    rotateZclock= "RZC"
    rotateZantiClock = "RZA"
    reset = "R"
    quit = "Q"
    #unknown = 0
    #zoomIn  = 1
    #zoomOut = 2
    #moveLeft = 3
    #moveRight = 4
    #moveUp   = 5
    #moveDown = 6
    #rotateXf = 7
    #rotateXb = 8
    #rotateYleft = 9
    #rotateYright = 10
    #rotateZclock= 11
    #rotateZantiClock = 12
    #reset = 13
    #quit = 14

__d = {
        "ZOOM_IN":Ops.zoomIn,
        "ZOOM_OUT":Ops.zoomOut,
        "MOVE_LEFT":Ops.moveLeft,
        "MOVE_RIGHT":Ops.moveRight,
        "MOVE_UP":Ops.moveUp,
        "MOVE_DOWN":Ops.moveDown,
        "REVOLVE_CLOCKWISE":Ops.rotateYleft,
        "REVOLVE_ANTICLOCKWISE":Ops.rotateYright,
        "TILT_FORWARD":Ops.rotateXf,
        "TILT_BACKWARD":Ops.rotateXb,
        "ROTATE_CLOCKWISE":Ops.rotateZclock,
        "ROTATE_ANTICLOCKWISE":Ops.rotateZantiClock,
        "RESET":Ops.reset,
        "QUIT":Ops.quit
        }


def fromText(operation):
    if operation == "BEGIN":
        return None
    return __d[operation]

action2axis = {Ops.zoomIn:2, Ops.zoomOut:2, Ops.moveLeft:0, Ops.moveRight:0,
        Ops.moveUp:1, Ops.moveDown:1, Ops.rotateXf:3, Ops.rotateXb:3, 
        Ops.rotateYright:4, Ops.rotateYleft:4, Ops.rotateZantiClock:5, Ops.rotateZclock:5}
def axisOfAction(action):
    '''return the axis of an action: 0->x, 1->y, 2->z, 3->ax, 4->ay, 5->az'''
    return action2axis[action]

action2direction = {Ops.zoomIn:-1, Ops.zoomOut:1, Ops.moveLeft:-1, Ops.moveRight:1,
        Ops.moveUp:1, Ops.moveDown:-1, Ops.rotateXf:1, Ops.rotateXb:-1, 
        Ops.rotateYright:1, Ops.rotateYleft:-1, Ops.rotateZantiClock:1, Ops.rotateZclock:-1}
def directionOfAction(action):
    '''return the direction of an action: -1 or 1'''
    return action2direction[action]
