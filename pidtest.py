#!/usr/bin/env python3
"""Hold a target speed with the PID and print what both wheels do.

WHEELS OFF THE GROUND for the first runs. The lab warns the controller
can oscillate or run away, so keep a hand near the stop button.

  python3 pidtest.py              hold 150 rpm with the gains in config
  python3 pidtest.py 120          hold 120 rpm
  python3 pidtest.py 120 0.002 0.004 0

The last form overrides Kp Ki Kd without editing config, which is what
you want while tuning. Ctrl+C stops it, so does the e-stop button.
"""

import sys
import time

import config
from estop import EStop
from rover import Rover, SpeedController, Wheel

TARGET = float(sys.argv[1]) if len(sys.argv) > 1 else 150.0
GAINS = tuple(float(a) for a in sys.argv[2:5]) if len(sys.argv) > 4 else None
DURATION = 15.0

estop = EStop()
rover = Rover(estop)
left = Wheel(config.ENCODER_PIN_A)
right = Wheel(config.ENCODER_PIN_B)
control = SpeedController(rover, left, right, GAINS)

kp, ki, kd = control.tunings
print(f"target {TARGET:.0f} rpm   Kp {kp}  Ki {ki}  Kd {kd}")
print("   t   left rpm  left duty   right rpm  right duty")

try:
    estop.arm()
    control.target(TARGET)
    start = time.monotonic()
    while time.monotonic() - start < DURATION:
        time.sleep(config.CONTROL_INTERVAL)
        (lr, ld), (rr, rd) = control.update()
        t = time.monotonic() - start
        print(f"{t:5.1f} {lr:10.1f} {ld:10.3f}  {rr:10.1f} {rd:10.3f}")
    control.stop()
finally:
    estop.close()
