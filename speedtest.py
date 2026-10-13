#!/usr/bin/env python3
"""Print both wheels' rotations and RPM once a second.

Turn a wheel by hand, or drive the rover, and watch the numbers.

UNPLUG BOTH MOTORS FROM THE DRIVER BEFORE TURNING THEM BY HAND. A
spun motor feeds current back into the DRV8833 and can damage it.

Run on the Pi:  python3 speedtest.py
Ctrl+C stops it.
"""

import time

import config
from rover import Wheel

INTERVAL = 1.0

left = Wheel(config.ENCODER_A)
right = Wheel(config.ENCODER_B)

print("  left rev   left rpm    right rev   right rpm")
while True:
    time.sleep(INTERVAL)
    lr, ls = left.rotations, left.speed()
    rr, rs = right.rotations, right.speed()
    print(f"{lr:10.2f} {ls:10.1f}   {rr:10.2f} {rs:10.1f}")
