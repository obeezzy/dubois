import RPi.GPIO as GPIO
from ...oscillators import Oscillator

class Indicator:
    def __init__(self, *, pins=(14, 16, 15)):
        self.pins = pins
        self.oscillators = None
        self._setup()

    def _setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pins, GPIO.OUT, initial=GPIO.LOW)

    def _stop_oscillators(self):
        if self.oscillators is not None:
            for osc in self.oscillators:
                osc.stop()

    def power_on(self, oscillators=tuple()):
        try:
            if not isinstance(oscillators, tuple):
                raise TypeError('"oscillators" argument must be of type "tuple".')
            if oscillators is not None and len(oscillators) > 3:
                raise OscillatorLimitExceededError()

            self._stop_oscillators()
            self.oscillators = oscillators

            self._setup()
            if oscillators is None \
                    or len(oscillators) is 0 \
                    or (len(oscillators) > 0 and oscillators[0] is None):
                GPIO.output(self.pins[0], GPIO.HIGH)
            elif len(oscillators) > 0 and oscillators[0] is not None:
                if oscillators is not None and not isinstance(oscillators[0], Oscillator):
                    raise TypeError('Expected object of type "Oscillator".')

                if oscillators[0].recipe().upper() == 'T':
                    GPIO.output(self.pins[0], GPIO.HIGH)
                elif oscillators[0].recipe() == '':
                    GPIO.output(self.pins[0], GPIO.LOW)
                else:
                    oscillators[0].start(pins=[self.pins[0]])

            if oscillators is None \
                    or len(oscillators) is 0 \
                    or (len(oscillators) > 1 and oscillators[1] is None):
                GPIO.output(self.pins[1], GPIO.HIGH)
            elif len(oscillators) > 1 and oscillators[1] is not None:
                if oscillators is not None and not isinstance(oscillators[1], Oscillator):
                    raise TypeError('Expected object of type "Oscillator".')

                if oscillators[1].recipe().upper() == 'T':
                    GPIO.output(self.pins[1], GPIO.HIGH)
                elif oscillators[1].recipe() == '':
                    GPIO.output(self.pins[1], GPIO.LOW)
                else:
                    oscillators[1].start(pins=[self.pins[1]])

            if oscillators is None \
                    or len(oscillators) is 0 \
                    or (len(oscillators) > 2 and oscillators[2] is None):
                GPIO.output(self.pins[2], GPIO.HIGH)
            elif len(oscillators) > 2 and oscillators[2] is not None:
                if oscillators is not None and not isinstance(oscillators[2], Oscillator):
                    raise TypeError('Expected object of type "Oscillator".')

                if oscillators[2].recipe().upper() == 'T':
                    GPIO.output(self.pins[2], GPIO.HIGH)
                elif oscillators[2].recipe() == '':
                    GPIO.output(self.pins[2], GPIO.LOW)
                else:
                    oscillators[2].start(pins=[self.pins[2]])
        except:
            self._stop_oscillators()
            raise

    def power_off(self):
        self._stop_oscillators()
        self._setup()
        GPIO.output(self.pins[0], GPIO.LOW)
        GPIO.output(self.pins[1], GPIO.LOW)
        GPIO.output(self.pins[2], GPIO.LOW)

class OscillatorLimitExceededError:
    def __str__(self):
        return 'Tuple of oscillators must be 3 or less in total.'
