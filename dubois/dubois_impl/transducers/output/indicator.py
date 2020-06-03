import time
import RPi.GPIO as GPIO
from dubois.oscillators import Oscillator

class Indicator:
    COLOR_COUNT = 3
    def __init__(self, pins=(14, 16, 15)):
        self.pins = pins
        self.oscillators = None
        self._setup()

    def _setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pins, GPIO.OUT, initial=GPIO.LOW)

    def _start_oscillator(self, oscillator, *, pin, timestamp=None):
        if oscillator.recipe().upper() == 'T':
            GPIO.output(pin, GPIO.HIGH)
        elif oscillator.recipe() == '':
            GPIO.output(pin, GPIO.LOW)
        else:
            oscillator.start(pins=[pin],
                                timestamp=timestamp)

    def _stop_oscillators(self):
        if self.oscillators is not None:
            for osc in self.oscillators:
                osc.stop()

    def power_on(self, *oscillators):
        try:
            if oscillators is not None and len(oscillators) > Indicator.COLOR_COUNT:
                raise ArgumentLimitExceededError(len(oscillators), Indicator.COLOR_COUNT)

            self._stop_oscillators()
            self.oscillators = tuple(oscillators)
            timestamp = int(time.time())

            self._setup()
            if oscillators is None \
                    or len(oscillators) is 0 \
                    or (len(oscillators) > 0 and oscillators[0] is None):
                GPIO.output(self.pins[0], GPIO.HIGH)
            elif len(oscillators) > 0 and oscillators[0] is not None:
                if oscillators is not None \
                        and not isinstance(oscillators[0], Oscillator):
                    raise TypeError('Expected object of type "Oscillator".')
                else:
                    self._start_oscillator(oscillators[0],
                                            pin=self.pins[0],
                                            timestamp=timestamp)
            if oscillators is None \
                    or len(oscillators) is 0 \
                    or (len(oscillators) > 1 and oscillators[1] is None):
                GPIO.output(self.pins[1], GPIO.HIGH)
            elif len(oscillators) > 1 and oscillators[1] is not None:
                if oscillators is not None \
                        and not isinstance(oscillators[1], Oscillator):
                    raise TypeError('Expected object of type "Oscillator".')
                else:
                    self._start_oscillator(oscillators[1],
                                            pin=self.pins[1],
                                            timestamp=timestamp)
            if oscillators is None \
                    or len(oscillators) is 0 \
                    or (len(oscillators) > 2 and oscillators[2] is None):
                GPIO.output(self.pins[2], GPIO.HIGH)
            elif len(oscillators) > 2 and oscillators[2] is not None:
                if oscillators is not None \
                        and not isinstance(oscillators[2], Oscillator):
                    raise TypeError('Expected object of type "Oscillator".')
                else:
                    self._start_oscillator(oscillators[2],
                                            pin=self.pins[2],
                                            timestamp=timestamp)
        except:
            self._stop_oscillators()
            raise

    def power_off(self):
        self._stop_oscillators()
        self._setup()
        for pin in self.pins:
            GPIO.output(pin, GPIO.LOW)

class ArgumentLimitExceededError(RuntimeError):
    def __init__(self, count, limit):
        self.count = count
        self.limit = limit
    def __str__(self):
        return f'Maximum number of arguments is {self.limit}, {self.count} supplied.'
