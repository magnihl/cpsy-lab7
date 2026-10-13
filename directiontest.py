#!/usr/bin/env python3
"""Drive both wheels forward briefly and report which way each counts.

WHEELS OFF THE GROUND.

The two motors face opposite ways on the chassis, so one encoder
counting negative while the rover drives forward is expected, not a
fault. The PID needs to know which.

Run on the Pi:  python3 directiontest.py
"""

import time

import config
from estop import EStop
from rover import disconnect, Rover, Wheel

DURATION = 1.5

estop = EStop()
rover = Rover(estop)
left = Wheel(config.ENCODER_PIN_A)
right = Wheel(config.ENCODER_PIN_B)

try:
    estop.arm()
    left.reset()
    right.reset()

    print(f"driving forward for {DURATION} s")
    rover.forward()
    time.sleep(DURATION)
    rover.stop()
    time.sleep(0.3)

    for name, wheel in (("left", left), ("right", right)):
        rev = wheel.rotations
        if rev > 0.05:
            way = "positive"
        elif rev < -0.05:
            way = "negative"
        else:
            way = "NO MOVEMENT"
        print(f"{name:6} {rev:7.2f} rev   {way}")
finally:
    estop.close()
    left.close()
    right.close()
    disconnect()
