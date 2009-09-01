require("random")
require("strict")

local function generateRandomValue(dist, params)
    local value 
    if dist == "lognormal" then
        local zeta, sigma = unpack(params)
        value = random.lognormal(zeta, sigma)
    end
    value = value or 1
    return value
end

local function chooseAction(continueTable, state)
    local choice = random.nextInt(3)
    print ("choice ", choice)
    if choice == 0 then
        return "ZOOM_IN"
    elseif choice == 1 then
        return "ZOOM_OUT"
    end
end

local function changeAction(changeTable, state)
    local choice = random.nextInt(2)
    if choice == 0 then
        return "MOVE_LEFT"
    else
        return "MOVE_RIGHT"
    end
end

local function chooseBeginAction(beginTable)
    return "ZOOM_IN"
end

local function outputActions(actions, state)
    local currentTime = state.currentTime
    for _, item in ipairs(actions) do
        local action, t = unpack(item)
        print(currentTime, action)
        currentTime = currentTime + t
    end
    return currentTime
end

local function generateTimes(timesTable, state)
    return 1
end

local function generateActionList(times, nextAction, dist, params)
    local actions = {}
    for i = 1, times do
        actions[i] = {nextAction, generateRandomValue(dist, params)}
    end
    return actions
end

local function updateState(state, nextAction, newTime)
    --update coordinate
    if nextAction == "RESET" then
        state.x = 0
        state.y = 0
        state.z = 0
        state.ax = 0
        state.ay = 0
        state.az = 0
    else
        local axis, value = unpack(lookupTable[nextAction])
        state[axis] = state[axis] + value
    end
    print(state.x, state.y, state.z, state.ax, state.ay, state.az)
    state.prevAction = nextAction
    state.currentTime = newTime
    return state
end


local function loop(state, endTime)
    if state.currentTime > endTime then
        return
    end
    local nextAction
    if state.prevAction and state.prevAction ~= "RESET" then
        nextAction =  chooseAction(config.continueTable, state)
        if not nextAction then
            nextAction = changeAction(config.changeTable, state)
        end
    else
        nextAction = chooseBeginAction(config.beginTable)
    end
    assert(nextAction)
    local times = generateTimes(config.timesTable, nextAction)
    local actionList = generateActionList(times, nextAction, 
                                          config.smallIntervalDistribution,
                                          config.smallIntervalParameters)
    local newTime = outputActions(actionList, state)
    local newState = updateState(state, nextAction, newTime)
    return loop(newState, endTime)
end

local function outputBeginTime()
    print(os.time(), "BEGIN")
end

local function outputQuitTime(t)
    print(t, "END")
end

function main()
    local sessionLength = generateRandomValue(config.sessionLengthDistribution,
                                              config.sessionLengthParameters)
    local startTime = generateRandomValue(config.startTimeDistribution,
                                          config.startTimeParameters)
    local endTime     = sessionLength

    local state = {x=0,y=0,z=0,ax=0,ay=0,az=0,prevAction=nil,currentTime = startTime}

    print(endTime)
    outputBeginTime()
    loop(state, endTime)
    local quitTime = generateRandomValue(config.quitTimeDistribution, 
                                      config.quitTimeParameters)
    outputQuitTime(state.currentTime + quitTime)
end

--dofile("config")
--

config = {
    sessionLengthDistribution = "lognormal",
    sessionLengthParameters = {10, 0.2},
    startTimeDistribution = "lognormal",
    startTimeParameters = {1, 0.1},
    quitTimeDistribution = "lognormal",
    quitTimeDistribution = {0.2, 0.1}
}

lookupTable = {
    ZOOM_IN     =   {"z",   -1},
    ZOOM_OUT    =   {"z",    1},
    MOVE_LEFT   =   {"x",   -1},
    MOVE_RIGHT  =   {"x",    1},
    MOVE_UP     =   {"y",   -1},
    MOVE_DOWN   =   {"z",    1},
    TILT_CLOCKWISE     = {"ax",   1},
    TILT_ANTICLOCKWISE = {"ax", -1},
    REVOLVE_CLOCKWISE  = {"ay",  1},
    REVOLVE_ANTICLOCKWISE={"ay", -1},
    ROTATE_CLOCKWISE   = {"az",  1},
    ROTATE_ANTICLOCKWISE = {"az", -1}
}

main()



