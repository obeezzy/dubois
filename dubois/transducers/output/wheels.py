import RPi.GPIO as GPIO

class Wheels(object):
    def __init__(self, *args, **kwargs):
        self.leftMotorPinPair = tuple(kwargs.get('leftMotorPinPair', (18, 23)))
        self.rightMotorPinPair = tuple(kwargs.get('rightMotorPinPair', (24, 25)))

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.leftMotorPinPair[0], GPIO.OUT)
        GPIO.setup(self.leftMotorPinPair[1], GPIO.OUT)
        GPIO.setup(self.rightMotorPinPair[0], GPIO.OUT)
        GPIO.setup(self.rightMotorPinPair[1], GPIO.OUT)

    def move_forward(self):
        self.stop()
        GPIO.output(self.leftMotorPinPair[1], GPIO.HIGH)
        GPIO.output(self.rightMotorPinPair[1], GPIO.HIGH)

    def move_in_reverse(self):
        self.stop()
        GPIO.output(self.leftMotorPinPair[0], GPIO.HIGH)
        GPIO.output(self.rightMotorPinPair[0], GPIO.HIGH)

    def move_counterclockwise(self):
        self.stop()
        GPIO.output(self.leftMotorPinPair[0], GPIO.HIGH)
        GPIO.output(self.rightMotorPinPair[1], GPIO.HIGH)

    def move_clockwise(self):
        self.stop()
        GPIO.output(self.leftMotorPinPair[1], GPIO.HIGH)
        GPIO.output(self.rightMotorPinPair[0], GPIO.HIGH)

    def stop(self):
        GPIO.output(self.leftMotorPinPair[0], GPIO.LOW)
        GPIO.output(self.leftMotorPinPair[1], GPIO.LOW)
        GPIO.output(self.rightMotorPinPair[0], GPIO.LOW)
        GPIO.output(self.rightMotorPinPair[1], GPIO.LOW)

    def shutdown(self):
        GPIO.cleanup()
