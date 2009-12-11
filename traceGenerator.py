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

def related_value(action, state):
    '''return the name of the related axis of an action'''
    axis = lookupTable[action][0]
    return state[axis]

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
    
    action = state["prevAction"]
    axis = related_axis(action)
    v =    related_value(action, state)
    
    #by default reverse
    p_continue, p_reverse = 0.5, 0.5
    try:
        count, p_continue, p_reverse, p_reset = continueDict[axis][v][action]
        #print "continue or not?:", axis, v, count, p_continue, p_reverse, p_reset
    except KeyError:
        print "Out of the range"
        pass #use the default value
    
    rand = random.nextDouble()
    #print "rand: ", rand, p_continue, p_continue+p_reverse, p_continue+p_reverse+p_reset
    if rand <= p_continue:
        return action
    elif rand <= p_continue + p_reverse:
        return reverseTable[action]
    elif rand <= p_continue + p_reverse + p_reset:
        return 'RESET'
    else:
        return 'CHANGE'

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

    rand = random.nextDouble() * acc_1_pop
    for ax, acc in acc_res:
        #print "rand: ", rand, "axis", ax, "acc ", acc
        if rand <= acc:
            return ax

def selectDirection(popPlus, popMinus):
    propPlus = popPlus / (popPlus + popMinus)
    rand = random.nextDouble()
    if rand < propPlus:
        return "plus"
    else:
        return "minus"



def changeAction(popularityDict, state):
    '''To decide a new direction when a decision is made to 
    change to a new direction rather than continue or reverse.

    the decision is based on the stability of the current state
    on each axis.'''
    axis = related_axis(state["prevAction"])
    popularity = {}
    popularityPlus   = {}
    popularityMinus  = {}
    for ax in ("x", "y", "z", "ax", "ay", "az"):
        v = state[ax]
        #print ax, v, popularityDict[ax][v], 1/popularityDict[ax][v]
        if ax != axis:
            popularity_curr = popularityDict[ax][v]
            #consider more steps
            popularity_plus = popularityDict[ax].get(v+1, 0)
            popularity_plus += popularityDict[ax].get(v+2, 0)
            popularity_plus += popularityDict[ax].get(v+3, 0)
            
            popularity_minus = popularityDict[ax].get(v-1, 0)
            popularity_minus += popularityDict[ax].get(v-2, 0)
            popularity_minus += popularityDict[ax].get(v-3, 0)
            
            popularity[ax] = popularity_curr
            popularityPlus[ax], popularityMinus[ax] = popularity_plus, popularity_minus
            #print "curr, plus, minus: ", popularity_curr, popularity_plus, popularity_minus

    selected_ax = selectAxis(popularity)
    #print "selected ax: ", selected_ax
    assert(selected_ax)

    #Next to select directon:
    if selectDirection(popularityPlus[selected_ax], popularityMinus[selected_ax]) == "plus":
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
    currentTime = state["currentTime"]
    for item in actions:
        action, t = item
        outputTrace(fout, currentTime, action)
        currentTime += t
    return currentTime

def generateTimes(timesDict, state):
    return 1

def generateActionList(times, nextAction, dist, params):
    actions = []
    actions.append((nextAction, 0))
    if times > 1:
        for i in range(times - 1):
            actions.append((nextAction, generateRandomValue(dist,params)))
    return actions

def updateTime(state, newTime):
    state["currentTime"] = newTime

def updateState(state, nextAction):
    '''update the state after an action is chosen.'''
    if nextAction == "RESET":
        reset(state)
    else:
        axis, value = lookupTable[nextAction]
        if axis in ("ax", "ay", "az"):
            state[axis] = (state[axis]+ value) % 36
        else:
            state[axis] += value

    state["prevAction"] = nextAction

def thinktime(time_lst):
    return random.choice(time_lst)

def loop(fout, state, endTime):
    '''keep choosing actions and updating the state until the session time
    is expired.'''
    nextAction = None
    while(state["currentTime"] < endTime):
        newTime = state["currentTime"]
        if state["prevAction"] != "BEGIN" and state["prevAction"] != "RESET":
            nextAction = chooseAction(config.continueDict, state)
            if nextAction == "CHANGE":
                nextAction = changeAction(config.popularityDict, state)
            if nextAction == state["prevAction"]:
                newTime += thinktime(config.continue_think_time_lst)
            else:
                newTime += thinktime(config.change_think_time_lst)
        else:
            nextAction = chooseBeginAction(config.beginDict)

        if state["prevAction"] != "BEGIN":
            updateTime(state, newTime) 

        assert(nextAction is not None)
        times = generateTimes(config.timesDict, nextAction)
        actionList = generateActionList(times, nextAction, config.smallIntervalDistribution,
                                                           config.smallIntervalParameters)

        newTime = outputActions(fout, actionList, state)
        if newTime > 0 :
            updateTime(state, newTime)
        
        updateState(state, nextAction)

def outputTrace(fout, t, action):
    sec = int(t) // 1000000
    msec =  int(t) - sec * 1000000
    print >>fout, sec, msec, action

def outputBeginTime(fout):
    outputTrace(fout, time.time(), "BEGIN")

def outputQuitTime(fout, t):
    outputTrace(fout, t, "QUIT")

def reset(state):
    state["x"] = 0
    state["y"] = 0
    state["z"] = 0
    state["ax"] = 0
    state["ay"] = 0
    state["az"] = 0

def init(state, startTime):
    reset(state)
    state["prevAction"] = "BEGIN"
    state["currentTime"] = startTime

class Config:
    pass

 
def main(fout, state):
    #choose session length (how long this session takes.
    sessionLength = generateRandomValue(config.sessionLengthDistribution,
                                        config.sessionLengthParameters)

    #choose how long before the first action is made.
    startTime     = generateRandomValue(config.startTimeDistribution,
                                        config.startTimeParameters)
    endTime       = sessionLength
    init(state, startTime)

    #print endTime
    outputBeginTime(fout)
    loop(fout, state, endTime)
    quitTime = generateRandomValue(config.quitTimeDistribution, config.quitTimeParameters)
    outputQuitTime(fout, state["currentTime"] + quitTime)
    
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
        config.popularityDict            = cPickle.load(input)
        config.continueDict              = cPickle.load(input)
        config.continue_think_time_lst   = cPickle.load(input)
        config.change_think_time_lst     = cPickle.load(input)
        config.timesDict                 = {}

    #revise popularityDict 
    #remove the effect of default viewpoint
    mz = config.popularityDict["z"]
    left = mz[3]
    right = mz[-1]
    diff  = left - right
    length = 4
    mz[2] = right + diff * 3. / 4.
    mz[1] = right + diff * 2. / 4.
    mz[0] = right + diff * 1. / 4.
    
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
            "y" : "MOVE_UP",
            "z" : "ZOOM_IN",
            "ax" : "TILT_BACKWARD",
            "ay" : "REVOLVE_ANTICLOCKWISE",
            "az" : "ROTATE_CLOCKWISE"
            }

    random.set_seed(0)
    state = {}
    if len(sys.argv) > 2:
        count = int(sys.argv[2])

        if len(sys.argv) > 3:
            prefix = sys.argv[3]

        for i in range(count):
            file_name = prefix + str(i) + ".trace"
            with open(file_name, "w") as f:
                main(f, state)
    else: #output to standard output
        main(sys.stdout, state)

    
            
                
    

        
