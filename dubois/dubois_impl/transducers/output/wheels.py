import RPi.GPIO as GPIO
import time
from enum import IntEnum, unique
from os import environ as env

@unique
class Direction(IntEnum):
    REVERSE = 0
    FORWARD = 1

class Wheels:
    def __init__(self, *,
                        left_wheel_pins=eval(env.get('LEFT_WHEEL_PINS', str((18, 23)))),
                        right_wheel_pins=eval(env.get('RIGHT_WHEEL_PINS', str((24, 25)))),
                        left_wheel_enable_pin=env.get('LEFT_WHEEL_ENABLE_PIN', 5),
                        right_wheel_enable_pin=env.get('RIGHT_WHEEL_ENABLE_PIN', 6)):
        self.left_wheel_pins = left_wheel_pins
        self.right_wheel_pins = right_wheel_pins
        self.left_wheel_enable_pin = left_wheel_enable_pin
        self.right_wheel_enable_pin = right_wheel_enable_pin
        self._setup()

    def _setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.left_wheel_pins, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.right_wheel_pins, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.left_wheel_enable_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.right_wheel_enable_pin, GPIO.OUT, initial=GPIO.LOW)

    def _enable_pins(self):
        GPIO.output(self.left_wheel_enable_pin, GPIO.HIGH)
        GPIO.output(self.right_wheel_enable_pin, GPIO.HIGH)

    def _disable_pins(self):
        GPIO.output(self.left_wheel_enable_pin, GPIO.LOW)
        GPIO.output(self.right_wheel_enable_pin, GPIO.LOW)

    def move_forward(self, *, timeout=2000):
        """Drives wheels to move in forward motion."""
        if not isinstance(timeout, int):
            raise InvalidTimeoutError()
        self._setup()
        GPIO.output(self.left_wheel_pins[Direction.FORWARD], GPIO.HIGH)
        GPIO.output(self.right_wheel_pins[Direction.FORWARD], GPIO.HIGH)
        self._enable_pins()
        if timeout > 0:
            time.sleep(timeout / 1000)
            self.stop()

    def move_backward(self, *, timeout=2000):
        """Drives wheels to move in backward motion."""
        if not isinstance(timeout, int):
            raise InvalidTimeoutError()
        self._setup()
        GPIO.output(self.left_wheel_pins[Direction.REVERSE], GPIO.HIGH)
        GPIO.output(self.right_wheel_pins[Direction.REVERSE], GPIO.HIGH)
        self._enable_pins()
        if timeout > 0:
            time.sleep(timeout / 1000)
            self.stop()

    def move_counterclockwise(self, *, timeout=2000):
        """Drives wheels to move in counterclockwise motion."""
        if not isinstance(timeout, int):
            raise InvalidTimeoutError()
        self._setup()
        GPIO.output(self.left_wheel_pins[Direction.REVERSE], GPIO.HIGH)
        GPIO.output(self.right_wheel_pins[Direction.FORWARD], GPIO.HIGH)
        self._enable_pins()
        if timeout > 0:
            time.sleep(timeout / 1000)
            self.stop()

    def move_clockwise(self, *, timeout=2000):
        """Drives wheels to move in clockwise motion."""
        if not isinstance(timeout, int):
            raise InvalidTimeoutError()
        self._setup()
        GPIO.output(self.left_wheel_pins[Direction.FORWARD], GPIO.HIGH)
        GPIO.output(self.right_wheel_pins[Direction.REVERSE], GPIO.HIGH)
        self._enable_pins()
        if timeout > 0:
            time.sleep(timeout / 1000)
            self.stop()

    def stop(self):
        """Ceases all motion."""
        self._setup()
        GPIO.output(self.left_wheel_pins, GPIO.LOW)
        GPIO.output(self.right_wheel_pins, GPIO.LOW)
        self._disable_pins()

class InvalidTimeoutError(RuntimeError):
    def __str__(self):
        return '"timeout" must be of type "int".'
