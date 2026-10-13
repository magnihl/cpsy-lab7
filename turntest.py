#!/usr/bin/env python3
"""Turn the rover by giving the two wheels different speeds.

Needs clear floor. An arc needs about half a metre, a spin needs only
the rover's own footprint, so try the spin first if space is tight.

  python3 turntest.py spin 80 3     wheels opposite, 80 rpm, 3 s
  python3 turntest.py arc 80 40 3   left 80, right 40, 3 s

Ctrl+C stops it, so does the e-stop button.
"""

import sys
import time

import config
from estop import EStop
from rover import Rover, SpeedController, Wheel, disconnect

mode = sys.argv[1] if len(sys.argv) > 1 else "spin"
if mode == "arc":
    left_t = float(sys.argv[2]) if len(sys.argv) > 2 else 80.0
    right_t = float(sys.argv[3]) if len(sys.argv) > 3 else 40.0
    duration = float(sys.argv[4]) if len(sys.argv) > 4 else 3.0
else:
    speed = float(sys.argv[2]) if len(sys.argv) > 2 else 80.0
    duration = float(sys.argv[3]) if len(sys.argv) > 3 else 3.0
    left_t, right_t = -speed, speed

estop = EStop()
rover = Rover(estop)
left = Wheel(config.ENCODER_PIN_A)
right = Wheel(config.ENCODER_PIN_B)
control = SpeedController(rover, left, right)

wanted = config.turn_rate_deg_s(left_t, right_t)
print(f"{mode}: left {left_t:+.0f} rpm, right {right_t:+.0f} rpm")
print(f"wanted turn rate {wanted:.0f} deg/s on a {config.TRACK_CM} cm track")
print("   t   left rpm   right rpm   deg/s")

try:
    estop.arm()
    control.target(left_t, right_t)
    start = time.monotonic()
    while time.monotonic() - start < duration:
        time.sleep(config.CONTROL_INTERVAL)
        (lr, _), (rr, _) = control.update()
        # measured speeds are unsigned, so put the commanded signs back
        signed_l = lr if left_t >= 0 else -lr
        signed_r = rr if right_t >= 0 else -rr
        rate = config.turn_rate_deg_s(signed_l, signed_r)
        print(f"{time.monotonic() - start:5.1f} {lr:10.1f} {rr:11.1f}"
              f" {rate:8.0f}")
    control.stop()
finally:
    estop.close()
    left.close()
    right.close()
    disconnect()
