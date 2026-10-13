MOTOR_A = {"forward": "GPIO12", "backward": "GPIO13"}
MOTOR_B = {"forward": "GPIO19", "backward": "GPIO18"}
ENCODER_A = ("GPIO5", "GPIO6")
ENCODER_B = ("GPIO16", "GPIO26")
SLEEP_PIN = "GPIO25"
STOP_PIN = "GPIO4"
IR_CHANNEL = 0

# one full rotation is about 700 encoder pulses, per the Lab 6 page.
# measured 1.04 and 1.13 rev for one hand turn, so 700 is close enough
PULSES_PER_REV = 700

# the motors face opposite ways on the chassis, so the right encoder
# counts backwards while the rover drives forward. measured 13 Oct
ENCODER_A_SIGN = 1
ENCODER_B_SIGN = -1

SPEED = 0.5

# the terminal waits before it starts repeating a held key, so the first
# press gets a long grace period and the rest get a short one
STOP_AFTER = 0.1
FIRST_HOLD = 0.7
REPEAT_GAP = 0.25

DEBOUNCE = 0.05
