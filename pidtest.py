#!/usr/bin/env python3
"""Hold a target speed with the PID and print what both wheels do.

WHEELS OFF THE GROUND for the first runs. The lab warns the controller
can oscillate or run away, so keep a hand near the stop button.

  python3 pidtest.py                    150 rpm for 15 s, config gains
  python3 pidtest.py 80                 80 rpm for 15 s
  python3 pidtest.py 80 4               80 rpm for 4 s
  python3 pidtest.py 80 4 0.002 0.004 0 and these gains

Arguments are target, duration, then Kp Ki Kd. Overriding the gains on
the command line means tuning does not need an edit and a push each
time.

On the floor, distance is target / 60 * duration wheel turns. 80 rpm for
4 s is about 5 turns, roughly a metre on a 65 mm wheel.

Ctrl+C stops it, so does the e-stop button.
"""

import sys
import time

import config
from estop import EStop
from rover import disconnect, Rover, SpeedController, Wheel

TARGET = float(sys.argv[1]) if len(sys.argv) > 1 else 150.0
DURATION = float(sys.argv[2]) if len(sys.argv) > 2 else 15.0
GAINS = tuple(float(a) for a in sys.argv[3:6]) if len(sys.argv) > 5 else None

estop = EStop()
rover = Rover(estop)
left = Wheel(config.ENCODER_PIN_A)
right = Wheel(config.ENCODER_PIN_B)
control = SpeedController(rover, left, right, GAINS)

kp, ki, kd = control.tunings
turns = TARGET / 60 * DURATION
print(f"target {TARGET:.0f} rpm for {DURATION:.0f} s, about {turns:.0f} "
      f"wheel turns   Kp {kp}  Ki {ki}  Kd {kd}")
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
    left.close()
    right.close()
    disconnect()
