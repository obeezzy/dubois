import RPi.GPIO as GPIO

class Headlights(object):
    def __init__(self, *, pin=7):
        self.pin = pin
        self.oscillator = None
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)

    def power_on(self, *, oscillator=None):
        if oscillator is None and self.oscillator is None:
            GPIO.output(self.pin, GPIO.HIGH)
        elif self.oscillator is None:
            self.oscillator = oscillator
            self.oscillator.start(pins=[self.pin])
        else:
            self.oscillator.stop()
            self.oscillator = oscillator
            self.oscillator.start(pins=[self.pin])

    def power_off(self):
        if self.oscillator is None:
            GPIO.output(self.pin, GPIO.LOW)
        else:
            self.oscillator.stop()
            self.oscillator = None

    def shutdown(self):
        GPIO.cleanup()
