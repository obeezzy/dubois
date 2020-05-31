import RPi.GPIO as GPIO
import time

class Wheels(object):
    def __init__(self, *args, **kwargs):
        self.leftMotorPinPair = tuple(kwargs.get('leftMotorPinPair', (18, 23)))
        self.rightMotorPinPair = tuple(kwargs.get('rightMotorPinPair', (24, 25)))
        self.leftMotorEnablePin = kwargs.get('leftMotorEnablePin', 5)
        self.rightMotorEnablePin = kwargs.get('rightMotorEnablePin', 6)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.leftMotorPinPair[0], GPIO.OUT)
        GPIO.setup(self.leftMotorPinPair[1], GPIO.OUT)
        GPIO.setup(self.rightMotorPinPair[0], GPIO.OUT)
        GPIO.setup(self.rightMotorPinPair[1], GPIO.OUT)

        GPIO.setup(self.leftMotorEnablePin, GPIO.OUT)
        GPIO.setup(self.rightMotorEnablePin, GPIO.OUT)

        self.stop()

    def move_forward(self, *, timeout=2000):
        """Drives wheels to move in forward motion."""
        if not isinstance(timeout, int):
            raise InvalidTimeoutError()
        GPIO.output(self.leftMotorPinPair[1], GPIO.HIGH)
        GPIO.output(self.rightMotorPinPair[1], GPIO.HIGH)
        GPIO.output(self.leftMotorEnablePin, GPIO.HIGH)
        GPIO.output(self.rightMotorEnablePin, GPIO.HIGH)
        if timeout > 0:
            time.sleep(timeout / 1000)
            self.stop()

    def move_backward(self, *, timeout=2000):
        """Drives wheels to move in backward motion."""
        if not isinstance(timeout, int):
            raise InvalidTimeoutError()
        GPIO.output(self.leftMotorPinPair[0], GPIO.HIGH)
        GPIO.output(self.rightMotorPinPair[0], GPIO.HIGH)
        GPIO.output(self.leftMotorEnablePin, GPIO.HIGH)
        GPIO.output(self.rightMotorEnablePin, GPIO.HIGH)
        if timeout > 0:
            time.sleep(timeout / 1000)
            self.stop()

    def move_counterclockwise(self, *, timeout=2000):
        """Drives wheels to move in counterclockwise motion."""
        if not isinstance(timeout, int):
            raise InvalidTimeoutError()
        GPIO.output(self.leftMotorPinPair[0], GPIO.HIGH)
        GPIO.output(self.rightMotorPinPair[1], GPIO.HIGH)
        GPIO.output(self.leftMotorEnablePin, GPIO.HIGH)
        GPIO.output(self.rightMotorEnablePin, GPIO.HIGH)
        if timeout > 0:
            time.sleep(timeout / 1000)
            self.stop()

    def move_clockwise(self, *, timeout=None):
        """Drives wheels to move in clockwise motion."""
        if not isinstance(timeout, int):
            raise InvalidTimeoutError()
        GPIO.output(self.leftMotorPinPair[1], GPIO.HIGH)
        GPIO.output(self.rightMotorPinPair[0], GPIO.HIGH)
        GPIO.output(self.leftMotorEnablePin, GPIO.HIGH)
        GPIO.output(self.rightMotorEnablePin, GPIO.HIGH)
        if timeout > 0:
            time.sleep(timeout / 1000)
            self.stop()

    def stop(self):
        """Ceases all motion."""
        GPIO.output(self.leftMotorPinPair[0], GPIO.LOW)
        GPIO.output(self.leftMotorPinPair[1], GPIO.LOW)
        GPIO.output(self.rightMotorPinPair[0], GPIO.LOW)
        GPIO.output(self.rightMotorPinPair[1], GPIO.LOW)
        GPIO.output(self.leftMotorEnablePin, GPIO.LOW)
        GPIO.output(self.rightMotorEnablePin, GPIO.LOW)

    def shutdown(self):
        """Shuts down this transducer."""
        self.stop()
        GPIO.cleanup()

class InvalidTimeoutError(Exception):
    def __str__(self):
        return "'timeout' must be of type 'int'.";
