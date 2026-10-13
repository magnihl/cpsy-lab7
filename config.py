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
# GPIO16 is motor B's C1 on paper but reads no edges at all, 13 Oct, so
# the right wheel uses C2 instead. likely a loose jumper on Pi pin 36.
# single channel counting does not care which of the two it uses
ENCODER_PIN_B = "GPIO26"

SLEEP_PIN = "GPIO25"
STOP_PIN = "GPIO4"
IR_CHANNEL = 0

# measured 13 Oct with calibrate.py over 5 hand turns per wheel:
# left 3475 edges, right 3450, so (3475 + 3450) / 10. the two agree to
# 0.7 percent, inside hand turning error, so one constant serves both.
# the Lab 6 page's "about 700 pulses" is one channel's rising edges,
# not the quadrature total
PULSES_PER_REV = 693

SPEED = 0.5

# the terminal waits before it starts repeating a held key, so the first
# press gets a long grace period and the rest get a short one
STOP_AFTER = 0.1
FIRST_HOLD = 0.7
REPEAT_GAP = 0.25

DEBOUNCE = 0.05
