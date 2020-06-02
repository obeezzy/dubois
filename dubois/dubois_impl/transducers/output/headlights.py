import RPi.GPIO as GPIO
from ...oscillators import Oscillator

class Headlights:
    def __init__(self, *, pin=7):
        self.pin = pin
        self.oscillator = None
        self._setup()

    def _setup(self):
        if GPIO.getmode() != GPIO.BCM:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)

    def power_on(self, oscillator=None):
        if oscillator is not None and not isinstance(oscillator, Oscillator):
            raise TypeError('"oscillator" argument must be of type "Oscillator".')

        self._setup()
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
        self._setup()
        if self.oscillator is None:
            GPIO.output(self.pin, GPIO.LOW)
        else:
            self.oscillator.stop()
            self.oscillator = None
