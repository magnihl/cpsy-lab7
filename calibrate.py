#!/usr/bin/env python3
"""Count raw encoder edges so PULSES_PER_REV can be measured.

Everything stays plugged in, run nothing else, the driver stays asleep.

Turn ONE wheel exactly 5 full turns in ONE direction, then read its
pulse count and divide by 5. The tally has no sign, so turning back the
other way adds to it rather than subtracting.

Run on the Pi:  python3 calibrate.py
Ctrl+C stops it.
"""

import time

import config
from rover import Wheel, disconnect

left = Wheel(config.ENCODER_PIN_A)
right = Wheel(config.ENCODER_PIN_B)
left.reset()
right.reset()

print("turn one wheel 5 full turns one way, then divide its count by 5")
print("  left pulses   right pulses")
try:
    while True:
        time.sleep(0.5)
        print(f"{left.pulses:13d} {right.pulses:14d}", end="\r", flush=True)
except KeyboardInterrupt:
    print()
finally:
    left.close()
    right.close()
    disconnect()
