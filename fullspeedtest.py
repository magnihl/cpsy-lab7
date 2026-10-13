#!/usr/bin/env python3
"""Drive forward at several duty levels and report the speed of each wheel.

WHEELS OFF THE GROUND.

Maps the plant: what duty produces what speed, where the motor stops
responding at the bottom, and how flat the top is. A PID tuned without
this works at one speed and oscillates at others.

Run on the Pi:  python3 fullspeedtest.py
"""

import time

import config
from estop import EStop
from rover import Rover, Wheel

DUTIES = (0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.5, 1.0)
SETTLE = 1.0
MEASURE = 2.0

estop = EStop()
rover = Rover(estop)
left = Wheel(config.ENCODER_PIN_A)
right = Wheel(config.ENCODER_PIN_B)

try:
    estop.arm()
    print(" duty    left rpm   right rpm")
    for duty in DUTIES:
        rover.forward(duty)
        time.sleep(SETTLE)
        left.speed()
        right.speed()
        time.sleep(MEASURE)
        print(f"{duty:5.2f} {left.speed():11.1f} {right.speed():11.1f}")
    rover.stop()
finally:
    estop.close()
