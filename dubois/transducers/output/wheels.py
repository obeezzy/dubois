import RPi.GPIO as GPIO
from threading import Timer

class Wheels(object):
    def __init__(self, *args, **kwargs):
        self.leftMotorPinPair = tuple(kwargs.get('leftMotorPinPair', (18, 23)))
        self.rightMotorPinPair = tuple(kwargs.get('rightMotorPinPair', (24, 25)))
        self.__timer = Timer(0, self.stop)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.leftMotorPinPair[0], GPIO.OUT)
        GPIO.setup(self.leftMotorPinPair[1], GPIO.OUT)
        GPIO.setup(self.rightMotorPinPair[0], GPIO.OUT)
        GPIO.setup(self.rightMotorPinPair[1], GPIO.OUT)

    def move_forward(self, timeout=None):
        self.stop()
        if timeout is not None:
            self.__timer.cancel()
            self.__timer = Timer(timeout, self.stop)
            self.__timer.start()
        elif timeout is not None and not isinstance(timeout, float):
            raise InvalidTimeoutError()
        GPIO.output(self.leftMotorPinPair[1], GPIO.HIGH)
        GPIO.output(self.rightMotorPinPair[1], GPIO.HIGH)

    def move_backward(self, timeout=None):
        self.stop()
        if timeout is not None:
            self.__timer.cancel()
            self.__timer = Timer(timeout, self.stop)
            self.__timer.start()
        elif timeout is not None and not isinstance(timeout, float):
            raise InvalidTimeoutError()
        GPIO.output(self.leftMotorPinPair[0], GPIO.HIGH)
        GPIO.output(self.rightMotorPinPair[0], GPIO.HIGH)

    def move_counterclockwise(self, timeout=None):
        self.stop()
        if timeout is not None:
            self.__timer.cancel()
            self.__timer = Timer(timeout, self.stop)
            self.__timer.start()
        elif timeout is not None and not isinstance(timeout, float):
            raise InvalidTimeoutError()
        GPIO.output(self.leftMotorPinPair[0], GPIO.HIGH)
        GPIO.output(self.rightMotorPinPair[1], GPIO.HIGH)

    def move_clockwise(self, timeout=None):
        self.stop()
        if timeout is not None:
            self.__timer.cancel()
            self.__timer = Timer(timeout, self.stop)
            self.__timer.start()
        elif timeout is not None and not isinstance(timeout, float):
            raise InvalidTimeoutError()
        GPIO.output(self.leftMotorPinPair[1], GPIO.HIGH)
        GPIO.output(self.rightMotorPinPair[0], GPIO.HIGH)

    def stop(self):
        GPIO.output(self.leftMotorPinPair[0], GPIO.LOW)
        GPIO.output(self.leftMotorPinPair[1], GPIO.LOW)
        GPIO.output(self.rightMotorPinPair[0], GPIO.LOW)
        GPIO.output(self.rightMotorPinPair[1], GPIO.LOW)

    def shutdown(self):
        GPIO.cleanup()

class InvalidTimeoutError(Exception):
    def __str__(self):
        return "'timeout' must be of type 'float'.";
