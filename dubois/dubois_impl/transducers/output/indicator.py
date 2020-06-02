import RPi.GPIO as GPIO
from threading import Timer

class Indicator(object):
    def __init__(self, *, pins=(15, 14, 16)):
        self.pins = pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pins, GPIO.OUT, initial=GPIO.LOW)

    def power_on(self, *, r=1.0, g=1.0, b=1.0):
        GPIO.output(self.pins[0], GPIO.HIGH)
        GPIO.output(self.pins[1], GPIO.HIGH)
        GPIO.output(self.pins[2], GPIO.HIGH)

    def power_off(self):
        GPIO.output(self.pins[0], GPIO.LOW)
        GPIO.output(self.pins[1], GPIO.LOW)
        GPIO.output(self.pins[2], GPIO.LOW)

    def shutdown(self):
        GPIO.cleanup()
