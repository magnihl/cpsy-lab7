MOTOR_A = {"forward": "GPIO12", "backward": "GPIO13"}
MOTOR_B = {"forward": "GPIO19", "backward": "GPIO18"}
ENCODER_A = ("GPIO5", "GPIO6")
ENCODER_B = ("GPIO16", "GPIO26")
SLEEP_PIN = "GPIO25"
STOP_PIN = "GPIO4"
IR_CHANNEL = 0

# one full rotation is about 700 encoder pulses, per the Lab 6 page
PULSES_PER_REV = 700

SPEED = 0.5

# the terminal waits before it starts repeating a held key, so the first
# press gets a long grace period and the rest get a short one
STOP_AFTER = 0.1
FIRST_HOLD = 0.7
REPEAT_GAP = 0.25

DEBOUNCE = 0.05
