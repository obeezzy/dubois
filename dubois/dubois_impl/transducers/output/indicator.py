import RPi.GPIO as GPIO
import time
from enum import IntEnum, unique
from os import environ as env
from dubois.oscillators import Oscillator

@unique
class Color(IntEnum):
    RED = 0
    GREEN = 1
    BLUE = 2

class Indicator:
    def __init__(self, pins=eval(env.get('INDICATOR_PINS', str((14, 16, 15))))):
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
                if osc is not None:
                    osc.stop()

    def power_on(self, *oscillators):
        try:
            if oscillators is not None and len(oscillators) > len(Color):
                raise ArgumentLimitExceededError(len(oscillators), len(Color))

            self._stop_oscillators()
            self.oscillators = tuple(oscillators)
            timestamp = int(time.time())

            self._setup()
            if oscillators is None \
                    or len(oscillators) is 0 \
                    or (len(oscillators) > 0 and oscillators[Color.RED] is None):
                GPIO.output(self.pins[Color.RED], GPIO.HIGH)
            elif len(oscillators) > 0 and oscillators[Color.RED] is not None:
                if oscillators is not None \
                        and not isinstance(oscillators[Color.RED], Oscillator):
                    raise TypeError('Expected object of type "Oscillator".')
                else:
                    self._start_oscillator(oscillators[Color.RED],
                                            pin=self.pins[Color.RED],
                                            timestamp=timestamp)
            if oscillators is None \
                    or len(oscillators) is 0 \
                    or (len(oscillators) > 1 and oscillators[Color.GREEN] is None):
                GPIO.output(self.pins[Color.GREEN], GPIO.HIGH)
            elif len(oscillators) > 1 and oscillators[Color.GREEN] is not None:
                if oscillators is not None \
                        and not isinstance(oscillators[Color.GREEN], Oscillator):
                    raise TypeError('Expected object of type "Oscillator".')
                else:
                    self._start_oscillator(oscillators[Color.GREEN],
                                            pin=self.pins[Color.GREEN],
                                            timestamp=timestamp)
            if oscillators is None \
                    or len(oscillators) is 0 \
                    or (len(oscillators) > 2 and oscillators[Color.BLUE] is None):
                GPIO.output(self.pins[Color.BLUE], GPIO.HIGH)
            elif len(oscillators) > 2 and oscillators[Color.BLUE] is not None:
                if oscillators is not None \
                        and not isinstance(oscillators[Color.BLUE], Oscillator):
                    raise TypeError('Expected object of type "Oscillator".')
                else:
                    self._start_oscillator(oscillators[Color.BLUE],
                                            pin=self.pins[Color.BLUE],
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
