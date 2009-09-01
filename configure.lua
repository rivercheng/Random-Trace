--This is the configuration file of the random trace generator
config = config or {}
config.start_distribution = "lognormal"
config.start_distribution_parameters = {0.1, 0.2}
config.actions = {"ZOOM_IN", "ZOOM_OUT", "MOVE_LEFT", "MOVE_RIGHT", "MOVE_UP", "MOVE_DOWN",
                  "TILT_CLOCKWISE", "TILT_ANTICLOCKWISE", "REVOLVE_CLOCKWISE", "REVOLVE_ANTICLOCKWISE",
                  "ROTATE_CLOCKWISE", "ROTATE_ANTICLOCKWISE"}
config.continueProb = {}
config.reverseProb
config.continueProb.MOVE_LEFT = {[-4]=0, [-3]=0.2, [-2]=0.223, [-1]=0.19, [0]=0.62, 0.40, 1,       1, 1, 1, 1, 1, 1, 1, 1, 1,   1, 1, 1}

config.continueProb.MOVE_RIGHT = {[-4]=1,[-3]=1,   [-2]=0,     [-1]=0.8,  [0]=0.3,  0.25, 0.24, 0.09, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 1, 0} 
