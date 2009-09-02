import extend_random as random
import time
import math

def generateRandomValue(dist, params):
    value = None
    if dist == "lognormal":
        miu, sigma = params
        value = random.lognormal(miu, sigma)
    elif dist == "genextreme":
        a, b, c = params
        value = random.genextreme(a, b, c)
    elif dist == "weibull":
        a, loc, scale = params
        value = random.weibull(a, loc, scale)
    elif dist == "constant":
        value = params
    return value

def chooseAction(continueDict, state):
    choice = random.nextInt(3)
    if choice == 0:
        return "ZOOM_IN"
    elif choice == 1:
        return "ZOOM_OUT"
    else:
        return None

def changeAction(changeDict, state):
    choice = random.nextInt(2)
    if choice == 0:
        return "MOVE_LEFT"
    else:
        return "MOVE_RIGHT"

def chooseBeginAction(beginDict):
    return "ZOOM_IN"


def outputActions(actions, state):
    currentTime = state.currentTime
    for item in actions:
        action, t = item
        print currentTime, action
        currentTime += t
    return currentTime

def generateTimes(timesDict, state):
    return 1

def generateActionList(times, nextAction, dist, params):
    actions = []
    for i in range(times):
        actions.append((nextAction, generateRandomValue(dist,params)))
    return actions

def updateState(state, nextAction, newTime):
    #update coordinates
    if nextAction == "RESET":
        state.reset()
    else:
        axis, value = lookupTable[nextAction]
        exec ("state."+axis+" += value")
    print(state.x, state.y, state.z, state.ax, state.ay, state.az)
    state.prevAction = nextAction
    state.currentTime = newTime
    return state

def loop(state, endTime):
    nextAction = None
    while(state.currentTime < endTime):
        if state.prevAction != "BEGIN" and state.prevAction != "RESET":
            nextAction = chooseAction(config.continueDict, state)
            if not nextAction:
                nextAction = changeAction(config.changeDict, state)
        else:
            nextAction = chooseBeginAction(config.beginDict)
        assert(nextAction is not None)
        times = generateTimes(config.timesDict, nextAction)
        actionList = generateActionList(times, nextAction, config.smallIntervalDistribution,
                                                           config.smallIntervalParameters)
        newTime = outputActions(actionList, state)
        newTime += generateRandomValue(config.intervalDistribution,
                                       config.intervalParameters)
        state = updateState(state, nextAction, newTime)

def outputBeginTime():
    print time.time(), "BEGIN"

def outputQuitTime(t):
    print t, "QUIT"

class State:
    def __init__(self, startTime):
        self.reset()
        self.prevAction = "BEGIN"
        self.currentTime = startTime

    def reset(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.ax = 0
        self.ay = 0
        self.az = 0

class Config:
    pass

 
def main():
    sessionLength = generateRandomValue(config.sessionLengthDistribution,
                                        config.sessionLengthParameters)
    startTime     = generateRandomValue(config.startTimeDistribution,
                                        config.startTimeParameters)
    endTime       = sessionLength
    state         = State(startTime)

    print endTime
    outputBeginTime()
    loop(state, endTime)
    quitTime = generateRandomValue(config.quitTimeDistribution, config.quitTimeParameters)
    outputQuitTime(state.currentTime + quitTime)
    
if __name__ == "__main__":
    config = Config()
    config.sessionLengthDistribution = "lognormal"
    config.sessionLengthParameters   = (0.75432, math.exp(18.23))
    config.startTimeDistribution     = "genextreme"
    config.startTimeParameters       = (-0.25772, 10281000, 1054700)
    config.quitTimeDistribution      = "constant"
    config.quitTimeParameters        = 0.2
    config.smallIntervalDistribution = "weibull"
    config.smallIntervalParameters   = (0.48351, 0, 372.66)
    config.intervalDistribution      = "genextreme"
    config.intervalParameters        = (-0.51, 266370, 199870)
    config.beginDict                 = {}
    config.timesDict                 = {}
    config.continueDict              = {}
    config.changeDict                = {}

    lookupTable = {
        "ZOOM_IN": ("z", -1),
        "ZOOM_OUT": ("z", 1),
        "MOVE_LEFT":("x", -1),
        "MOVE_RIGHT": ("x", 1),
        "MOVE_UP": ("y", -1),
        "MOVE_DOWN": ("y", 1),
        "TILT_CLOCKWISE" : ("ax",   1),
        "TILT_ANTICLOCKWISE" : ("ax", -1),
        "REVOLVE_CLOCKWISE"  : ("ay",  1),
        "REVOLVE_ANTICLOCKWISE" :("ay", -1),
        "ROTATE_CLOCKWISE"   : ("az",  1),
        "ROTATE_ANTICLOCKWISE" : ("az", -1)
        }
    
    main()

    
            
                
    

        
