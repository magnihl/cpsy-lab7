"""The rover's drive and its wheel encoders."""

import time

import config  # sets the pin factory, import before gpiozero

import pigpio
from gpiozero import Motor, Robot

_pi = None


def _connect():
    """One shared pigpio connection for every wheel."""
    global _pi
    if _pi is None:
        _pi = pigpio.pi()
        if not _pi.connected:
            raise RuntimeError(
                "pigpiod is not running. "
                "sudo systemctl enable --now pigpiod"
            )
    return _pi


class Wheel:
    """Odometer and speedometer for one wheel.

    Counts rising edges on one encoder channel using pigpio's tally,
    which is kept in C and never calls back into Python. gpiozero's
    RotaryEncoder decodes quadrature in Python and tops out around 2300
    edges a second across all four pins, well below what these motors
    produce.

    The tally only ever increases, so distance and speed are unsigned.
    The caller knows which way it commanded the motor.
    """

    def __init__(self, pin, pulses_per_rev=config.PULSES_PER_REV):
        pi = _connect()
        # pigpio takes BCM numbers, config stores gpiozero's GPIOnn form
        self._gpio = int(pin.replace("GPIO", ""))
        pi.set_mode(self._gpio, pigpio.INPUT)
        pi.set_pull_up_down(self._gpio, pigpio.PUD_UP)
        # no function, so pigpio keeps the count itself
        self._cb = pi.callback(self._gpio, pigpio.RISING_EDGE)
        self._ppr = pulses_per_rev
        self._origin = 0
        self._last_count = 0
        self._last_time = time.monotonic()

    @property
    def pulses(self):
        """Raw edges since the last reset. Used for calibration."""
        return self._cb.tally() - self._origin

    @property
    def rotations(self):
        return self.pulses / self._ppr

    def speed(self):
        """Rotations per minute since the last call to speed().

        Measured by sampling, so call it on a steady interval. A longer
        interval is less noisy but slower to react.
        """
        now = time.monotonic()
        count = self._cb.tally()

        elapsed = now - self._last_time
        moved = count - self._last_count

        self._last_time = now
        self._last_count = count

        if elapsed <= 0:
            return 0.0
        return (moved / self._ppr) / elapsed * 60

    def reset(self):
        self._origin = self._cb.tally()
        self._last_count = self._origin
        self._last_time = time.monotonic()

    def close(self):
        self._cb.cancel()


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
