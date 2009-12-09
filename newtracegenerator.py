from __future__ import with_statement
import extend_random as random
import time
import math
import cPickle
import sys

def generateRandomValue(dist, params):
    '''Generate a random value following the given
    distribution.'''
    value = None
    if dist == "lognormal":
        sigma, scale = params
        value = random.lognormal(sigma, scale)
    elif dist == "genextreme":
        a, b, c = params
        value = random.genextreme(a, b, c)
    elif dist == "weibull":
        a, loc, scale = params
        value = random.weibull(a, loc, scale)
    elif dist == "constant":
        value = params
    return value

def related_value(action):
    '''return the name of the related axis of an action'''
    axis = lookupTable[action][0]
    return "state."+axis

def related_axis(action):
    '''return the name of the related axis of an action'''
    return lookupTable[action][0]

def chooseAction(continueDict, state):
    '''To choose whether to continue the previous direction,
    reverse the direction, or go to another direction.
    
    The decision is based on previous action and the 
    current state. For example, if previous action is 'ZOOM IN',
    then we only examine the 'z' value. The continueDict will give
    a probability to continue and a probability to reverse for each
    possible 'z' value.'''
    
    action = state.prevAction
    axis = related_axis(action)
    v = eval(related_value(action))
    
    #by default reverse
    p_continue, p_reverse = 0.5, 0.5
    try:
        p_continue, p_reverse = continueDict[axis][v][action]
        print 'cont', p_continue, 'rev', p_reverse
    except KeyError:
        pass #use the default value
    
    rand = random.nextDouble()
    if rand <= p_continue:
        return action
        print 'to contiue'
    #elif rand <= p_continue + p_reverse:
    #    return reverseTable[action]
    else:
        return None

def rateMove(popularity_curr, popularity_plus, popularity_minus):
    ratePlus = popularity_plus / popularity_curr
    rateMinus = popularity_minus / popularity_curr
    return ratePlus, rateMinus

def selectAxis(popularity):
    '''Choose the next axis to go along
    
    We add 1/popularity together, and choose the axis
    propotional to its 1/popularity. Exception: if the
    popularity of an axis is 0, we directly choose it.
    '''
    acc_1_pop = 0
    acc_res = []
    
    for ax, pop in popularity.iteritems():
        if (pop == 0):
            return ax
        acc_1_pop += (1 / pop)
        acc_res.append((ax, acc_1_pop))
        print ax, pop, 1 / pop

    rand = random.nextDouble() * acc_1_pop
    for ax, acc in acc_res:
        if rand <= acc:
            return ax

def selectDirection(ratePlus, rateMinus):
    propPlus = ratePlus / (ratePlus + rateMinus)
    rand = random.nextDouble()
    if rand < propPlus:
        return "plus"
    else:
        return "minus"



def changeAction(changeDict, state):
    '''To decide a new direction when a decision is made to 
    change to a new direction rather than continue or reverse.

    the decision is based on the stability of the current state
    on each axis.'''

    
    axis = related_axis(state.prevAction)
    popularity = {}
    ratePlus   = {}
    rateMinus  = {}
    for ax in ("x", "y", "z", "ax", "ay", "az"):
        #if ax != axis:
            v = eval("state."+ax)
            popularity_curr = changeDict[ax].get(v, 0)
            if popularity_curr == 0:
                return reverseTable[state.prevAction]

            #consider further more steps
            popularity_plus = changeDict[ax].get(v+1, 0)
            popularity_plus += changeDict[ax].get(v+2, 0)
            popularity_plus += changeDict[ax].get(v+3, 0)
            
            popularity_minus = changeDict[ax].get(v-1, 0)
            popularity_minus += changeDict[ax].get(v-2, 0)
            popularity_minus += changeDict[ax].get(v-3, 0)
            
            popularity[ax] = popularity_curr
            ratePlus[ax], rateMinus[ax] = rateMove(popularity_curr, popularity_plus, popularity_minus)

    selected_ax = selectAxis(popularity)
    assert(selected_ax)

    #Next to select directon:
    #if selected_ax == axis:
    #    return reverseTable[state.prevAction]

    if selectDirection(ratePlus[selected_ax], rateMinus[selected_ax]) == "plus":
        return plusAction[selected_ax]
    else:
        return reverseTable[plusAction[selected_ax]]

def chooseBeginAction(beginDict):
    '''In the beginning or after 'RESET', choose the first action
    at the default view point.'''
    accu_dict = {}
    sum = 0
    for action in sorted(beginDict.keys()):
        prob = beginDict[action]
        #print action, prob
        sum += prob
        accu_dict[action] = sum
        #print action, sum

    prob = random.nextDouble()
    for action in sorted(accu_dict.keys()):
        accu = accu_dict[action]
        #print action, accu, prob
        if prob <= accu:
            #print prob, "action ", action
            return action

def outputActions(fout, actions, state):
    currentTime = state.currentTime
    for item in actions:
        action, t = item
        outputTrace(fout, currentTime, action)
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
    '''update the state after an action is chosen.'''
    if nextAction == "RESET":
        state.reset()
    else:
        axis, value = lookupTable[nextAction]
        if axis in ("ax", "ay", "az"):
            exec ("state."+axis+" = (state."+axis+"+ value) % 36")
        else:
            exec ("state."+axis+" += value")

    state.prevAction = nextAction
    state.currentTime = newTime
    return state

def loop(fout, state, endTime):
    '''keep choosing actions and updating the state until the session time
    is expired.'''
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
        newTime = outputActions(fout, actionList, state)
        newTime += generateRandomValue(config.intervalDistribution,
                                       config.intervalParameters)
        state = updateState(state, nextAction, newTime)

def outputTrace(fout, t, action):
    sec = int(t) // 1000000
    msec =  int(t) - sec * 1000000
    print >>fout, sec, msec, action

def outputBeginTime(fout):
    outputTrace(fout, time.time(), "BEGIN")

def outputQuitTime(fout, t):
    outputTrace(fout, t, "QUIT")

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

 
def main(fout):
    #choose session length (how long this session takes.
    sessionLength = generateRandomValue(config.sessionLengthDistribution,
                                        config.sessionLengthParameters)

    #choose how long before the first action is made.
    startTime     = generateRandomValue(config.startTimeDistribution,
                                        config.startTimeParameters)
    endTime       = sessionLength
    state         = State(startTime)

    #print endTime
    outputBeginTime(fout)
    loop(fout, state, endTime)
    quitTime = generateRandomValue(config.quitTimeDistribution, config.quitTimeParameters)
    outputQuitTime(fout, state.currentTime + quitTime)
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage "+sys.argv[0]+ " <pickle file> [count] [prefix]"
        sys.exit()

    config = Config()
    #Session length follows the lognormal distribution.
    config.sessionLengthDistribution = "lognormal"
    config.sessionLengthParameters   = (0.75432, math.exp(18.23))

    #the inital time follows the general extreme distribution.
    config.startTimeDistribution     = "genextreme"
    config.startTimeParameters       = (-0.25772, 10281000, 1054700)

    config.quitTimeDistribution      = "constant"
    config.quitTimeParameters        = 0.2

    config.smallIntervalDistribution = "weibull"
    config.smallIntervalParameters   = (0.48351, 0, 372.66)
    
    config.intervalDistribution      = "genextreme"
    config.intervalParameters        = (-0.51, 266370, 199870)

    with open(sys.argv[1]) as input:
        config.beginDict                 = cPickle.load(input)
        config.changeDict                = cPickle.load(input)
        config.continueDict              = cPickle.load(input)
        config.timesDict                 = {}
    
    #print config.beginDict
    #print config.changeDict
    #print config.continueDict

    #Define the effect of each possible action (except RESET).
    lookupTable = {
        "ZOOM_IN": ("z", 1),
        "ZOOM_OUT": ("z", -1),
        "MOVE_LEFT":("x", -1),
        "MOVE_RIGHT": ("x", 1),
        "MOVE_UP": ("y", 1),
        "MOVE_DOWN": ("y", -1),
        "TILT_FORWARD" : ("ax",  -1),
        "TILT_BACKWARD" : ("ax", 1),
        "REVOLVE_CLOCKWISE"  : ("ay",  -1),
        "REVOLVE_ANTICLOCKWISE" :("ay", 1),
        "ROTATE_CLOCKWISE"   : ("az",  1),
        "ROTATE_ANTICLOCKWISE" : ("az", -1)
        }

    reverseTable = {
        "ZOOM_IN": "ZOOM_OUT",
        "MOVE_LEFT": "MOVE_RIGHT",
        "MOVE_UP": "MOVE_DOWN",
        "TILT_FORWARD" : "TILT_BACKWARD",
        "REVOLVE_CLOCKWISE"  : "REVOLVE_ANTICLOCKWISE",
        "ROTATE_CLOCKWISE"   : "ROTATE_ANTICLOCKWISE"
        }

    for k, v in list(reverseTable.iteritems()):
        reverseTable[v] = k
    

    plusAction = {
            "x" : "MOVE_RIGHT",
            "y" : "MOVE_DOWN",
            "z" : "ZOOM_IN",
            "ax" : "TILT_BACKWARD",
            "ay" : "REVOLVE_ANTICLOCKWISE",
            "az" : "ROTATE_CLOCKWISE"
            }

    random.set_seed(0)
    if len(sys.argv) > 2:
        count = int(sys.argv[2])

        if len(sys.argv) > 3:
            prefix = sys.argv[3]

        for i in range(count):
            file_name = prefix + str(i) + ".trace"
            with open(file_name, "w") as f:
                main(f)
    
    else: #output to standard output
        main(sys.stdout)

    
            
                
    

        
