import os

# gpiozero resolves this when the first device is created, so setting it
# here is enough as long as config is imported before any device exists.
# pigpio also gives DMA timed PWM instead of CPU timed.
os.environ.setdefault("GPIOZERO_PIN_FACTORY", "pigpio")

MOTOR_A = {"forward": "GPIO12", "backward": "GPIO13"}
MOTOR_B = {"forward": "GPIO19", "backward": "GPIO18"}

# both encoder channels, kept for reference. we no longer read the B
# channel: decoding quadrature in Python could not keep up, see
# ENCODER_PIN_A below
ENCODER_A = ("GPIO5", "GPIO6")
ENCODER_B = ("GPIO16", "GPIO26")

# C1 only, one channel per wheel. counted by pigpio's tally in C, which
# never wakes Python. no direction, the commanded direction gives that
ENCODER_PIN_A = "GPIO5"
ENCODER_PIN_B = "GPIO16"

SLEEP_PIN = "GPIO25"
STOP_PIN = "GPIO4"
IR_CHANNEL = 0

# NEEDS RECALIBRATING. 700 was the quadrature figure from the Lab 6
# page. Counting one channel's rising edges gives a different number.
# Run calibrate.py, turn a wheel 5 times one way, divide by 5.
PULSES_PER_REV = 700

SPEED = 0.5

# the terminal waits before it starts repeating a held key, so the first
# press gets a long grace period and the rest get a short one
STOP_AFTER = 0.1
FIRST_HOLD = 0.7
REPEAT_GAP = 0.25

DEBOUNCE = 0.05
