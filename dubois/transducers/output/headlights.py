import RPi.GPIO as GPIO

class Headlights(object):
    def __init__(self, *args, **kwargs):
        self.pin = kwargs.get('pin', 7)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def power_on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def power_off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def shutdown(self):
        GPIO.cleanup()
