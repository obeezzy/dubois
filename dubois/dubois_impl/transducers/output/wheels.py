import RPi.GPIO as GPIO
import time

class Wheels:
    def __init__(self, *,
                        leftMotorPinPair=(18, 23),
                        rightMotorPinPair=(24, 25),
                        leftMotorEnablePin=5,
                        rightMotorEnablePin=6):
        self.leftMotorPinPair = leftMotorPinPair
        self.rightMotorPinPair = rightMotorPinPair
        self.leftMotorEnablePin = leftMotorEnablePin
        self.rightMotorEnablePin = rightMotorEnablePin
        self._setup()

    def _setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.leftMotorPinPair, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.rightMotorPinPair, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.leftMotorEnablePin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.rightMotorEnablePin, GPIO.OUT, initial=GPIO.LOW)

    def _enable_pins(self):
        GPIO.output(self.leftMotorEnablePin, GPIO.HIGH)
        GPIO.output(self.rightMotorEnablePin, GPIO.HIGH)

    def _disable_pins(self):
        GPIO.output(self.leftMotorEnablePin, GPIO.LOW)
        GPIO.output(self.rightMotorEnablePin, GPIO.LOW)

    def move_forward(self, *, timeout=2000):
        """Drives wheels to move in forward motion."""
        if not isinstance(timeout, int):
            raise InvalidTimeoutError()
        self._setup()
        GPIO.output(self.leftMotorPinPair[1], GPIO.HIGH)
        GPIO.output(self.rightMotorPinPair[1], GPIO.HIGH)
        self._enable_pins()
        if timeout > 0:
            time.sleep(timeout / 1000)
            self.stop()

    def move_backward(self, *, timeout=2000):
        """Drives wheels to move in backward motion."""
        if not isinstance(timeout, int):
            raise InvalidTimeoutError()
        self._setup()
        GPIO.output(self.leftMotorPinPair[0], GPIO.HIGH)
        GPIO.output(self.rightMotorPinPair[0], GPIO.HIGH)
        self._enable_pins()
        if timeout > 0:
            time.sleep(timeout / 1000)
            self.stop()

    def move_counterclockwise(self, *, timeout=2000):
        """Drives wheels to move in counterclockwise motion."""
        if not isinstance(timeout, int):
            raise InvalidTimeoutError()
        self._setup()
        GPIO.output(self.leftMotorPinPair[0], GPIO.HIGH)
        GPIO.output(self.rightMotorPinPair[1], GPIO.HIGH)
        self._enable_pins()
        if timeout > 0:
            time.sleep(timeout / 1000)
            self.stop()

    def move_clockwise(self, *, timeout=None):
        """Drives wheels to move in clockwise motion."""
        if not isinstance(timeout, int):
            raise InvalidTimeoutError()
        self._setup()
        GPIO.output(self.leftMotorPinPair[1], GPIO.HIGH)
        GPIO.output(self.rightMotorPinPair[0], GPIO.HIGH)
        self._enable_pins()
        if timeout > 0:
            time.sleep(timeout / 1000)
            self.stop()

    def stop(self):
        """Ceases all motion."""
        self._setup()
        GPIO.output(self.leftMotorPinPair, GPIO.LOW)
        GPIO.output(self.rightMotorPinPair, GPIO.LOW)
        self._disable_pins()

class InvalidTimeoutError(Exception):
    def __str__(self):
        return "'timeout' must be of type 'int'.";
