#!/usr/bin/env python3
"""Drive forward at several duty levels and report the speed of each wheel.

WHEELS OFF THE GROUND.

Tells you the usable speed range before any PID is tuned against it.

Run on the Pi:  python3 fullspeedtest.py
"""

import time

import config
from estop import EStop
from rover import Rover, Wheel

DUTIES = (0.3, 0.5, 0.7, 1.0)
SETTLE = 1.0
MEASURE = 2.0

estop = EStop()
rover = Rover(estop)
left = Wheel(config.ENCODER_A, config.ENCODER_A_SIGN)
right = Wheel(config.ENCODER_B, config.ENCODER_B_SIGN)

try:
    estop.arm()
    print(" duty    left rpm   right rpm")
    for duty in DUTIES:
        rover.forward(duty)
        time.sleep(SETTLE)
        left.speed()
        right.speed()
        time.sleep(MEASURE)
        print(f"{duty:5.1f} {left.speed():11.1f} {right.speed():11.1f}")
    rover.stop()
finally:
    estop.close()
