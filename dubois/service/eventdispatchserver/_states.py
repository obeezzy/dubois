import json
from itertools import accumulate
import _logging as logging

logger = logging.getLogger(__name__)

class State(object):
    def __init__(self, category, action):
        self.action = action
        self.category = category

class BuzzerState(State):
    def __init__(self, action, buzzer):
        super().__init__('buzzer', action)
        self._buzzer = buzzer
        self.pin_active = False
        if action == 'power_on':
            self.pin_active = True
        elif action == 'power_off':
            self.pin_active = False

    def __str__(self):
        return (f'BuzzerState(pin_active={self.pin_active}, '
                f'oscillator={str(self._buzzer.oscillator)})')

    def __iter__(self):
        return iter({
            'category': self.category,
            'pinActive': self.pin_active,
            'oscillator': dict(self._buzzer.oscillator) \
                            if self._buzzer.oscillator is not None \
                            else None
        }.items())

class HeadlightState(State):
    def __init__(self, action, headlights):
        super().__init__('headlight', action)
        self._headlights = headlights
        self.pin_active = False
        if action == 'power_on':
            self.pin_active = True
        elif action == 'power_off':
            self.pin_active = False

    def __str__(self):
        return (f'HeadlightState(pin_active={self.pin_active}, '
                f'oscillator={str(self._headlights.oscillator)})')

    def __iter__(self):
        return iter({
            'category': self.category,
            'pinActive': self.pin_active,
            'oscillator': dict(self._headlights.oscillator) \
                            if self._headlights.oscillator is not None \
                            else None
        }.items())

class IndicatorState(State):
    def __init__(self, action, indicator):
        super().__init__('indicator', action)
        self._indicator = indicator
        self.pins_active = (False, False, False)
        if action == 'power_on':
            self.pins_active = (True, True, True)
        elif action == 'power_off':
            self.pins_active = (False, False, False)

    def __str__(self):
        return (f'IndicatorState(pins_active={str(self.pins_active)}, '
                f'oscillators={str(self._indicator.oscillators)})')

    def __iter__(self):
        return iter({
            'category': self.category,
            'pinsActive': self.pins_active,
            'oscillators': list(accumulate(dict(self._indicator.oscillators)))
                            if self._indicator.oscillators is not None \
                            else None
        }.items())
