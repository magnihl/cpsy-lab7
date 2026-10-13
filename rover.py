"""The rover's drive and its wheel encoders."""

import time

from gpiozero import Motor, Robot, RotaryEncoder

import config


class Wheel:
    """Odometer and speedometer for one wheel.

    Counts encoder pulses and reports distance in rotations and speed
    in rotations per minute.
    """

    def __init__(self, pins, sign=1, pulses_per_rev=config.PULSES_PER_REV):
        self._encoder = RotaryEncoder(*pins, max_steps=0)
        self._ppr = pulses_per_rev
        # +1 or -1, so forward reads positive on both sides
        self._sign = sign
        self._last_steps = 0
        self._last_time = time.monotonic()

    @property
    def rotations(self):
        """Total rotations since start. Negative means backwards."""
        return self._sign * self._encoder.steps / self._ppr

    def speed(self):
        """Rotations per minute since the last call to speed().

        Measured by sampling the count, so call it on a steady interval.
        A longer interval is less noisy but slower to react, which
        matters once a PID is reading this.
        """
        now = time.monotonic()
        steps = self._sign * self._encoder.steps

        elapsed = now - self._last_time
        moved = steps - self._last_steps

        self._last_time = now
        self._last_steps = steps

        if elapsed <= 0:
            return 0.0
        return (moved / self._ppr) / elapsed * 60

    def reset(self):
        self._encoder.steps = 0
        self._last_steps = 0
        self._last_time = time.monotonic()


class Rover:
    def __init__(self, estop, motor_a=config.MOTOR_A, motor_b=config.MOTOR_B):
        self._robot = Robot(left=Motor(**motor_a), right=Motor(**motor_b))
        self._estop = estop

    def forward(self, speed=config.SPEED):
        self._drive(self._robot.forward, speed)

    def backward(self, speed=config.SPEED):
        self._drive(self._robot.backward, speed)

    def left(self, speed=config.SPEED):
        self._drive(self._robot.left, speed)

    def right(self, speed=config.SPEED):
        self._drive(self._robot.right, speed)

    def stop(self):
        self._robot.stop()

    def _drive(self, action, speed):
        if not self._estop.armed:
            return
        action(speed)
