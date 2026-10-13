#!/usr/bin/env python3
"""Drive at full duty for 10 s and report counted revolutions.

WHEELS OFF THE GROUND. Put a piece of tape on the left tyre and count
how many times it comes round by eye, then compare with the number
printed. If the eye count is much higher, the encoder is losing pulses.

Run on the Pi:  python3 ceilingtest.py
"""

import time

import config
from estop import EStop
from rover import Rover, Wheel

DURATION = 10.0

estop = EStop()
rover = Rover(estop)
left = Wheel(config.ENCODER_PIN_A)
right = Wheel(config.ENCODER_PIN_B)

try:
    estop.arm()
    left.reset()
    right.reset()
    print(f"full duty for {DURATION:.0f} s, count the tape by eye")
    rover.forward(1.0)
    time.sleep(DURATION)
    rover.stop()
    time.sleep(0.5)
    print(f"counted   left {left.rotations:6.2f} rev   "
          f"right {right.rotations:6.2f} rev")
    print(f"          left {left.rotations / DURATION * 60:6.1f} rpm  "
          f"right {right.rotations / DURATION * 60:6.1f} rpm")
finally:
    estop.close()
