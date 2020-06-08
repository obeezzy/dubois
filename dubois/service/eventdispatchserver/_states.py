import json
from itertools import accumulate
import _logging as logging

logger = logging.getLogger(__name__)

class State(object):
    def __init__(self, category):
        self.category = category
        self._last_action = ''

    @property
    def last_action(self):
        return self._last_action

    @last_action.setter
    def last_action(self, action):
        self._last_action = action

class AggregateState(State):
    def __init__(self, *,
                    buzzer,
                    headlights,
                    indicator):
        super().__init__(category='aggregate')
        self.buzzer_state = BuzzerState(buzzer=buzzer)
        self.headlight_state = HeadlightState(headlights=headlights)
        self.indicator_state = IndicatorState(indicator=indicator)

    def __iter__(self):
        return iter({
            'category': self.category,
            'states': {
                'buzzer': dict(self.buzzer_state),
                'headlight': dict(self.headlight_state),
                'indicator': dict(self.indicator_state),
            },
        }.items())

class BuzzerState(State):
    def __init__(self, buzzer=None):
        super().__init__(category='buzzer')
        self._buzzer = buzzer
        self.pin_active = False

    @property
    def last_action(self):
        return self._last_action

    @last_action.setter
    def last_action(self, action):
        if action == 'power_on':
            self.pin_active = True
        elif action == 'power_off':
            self.pin_active = False

        self._last_action = action

    def __str__(self):
        oscillator = str(self._buzzer.oscillator \
                        if self._buzzer is not None \
                        else None)
        return (f'BuzzerState(pin_active={self.pin_active}, '
                f'oscillator={oscillator})')

    def __iter__(self):
        return iter({
            'category': self.category,
            'pinActive': self.pin_active,
            'oscillator': dict(self._buzzer.oscillator) \
                            if self._buzzer is not None \
                            and self._buzzer.oscillator is not None \
                            else None
        }.items())

class HeadlightState(State):
    def __init__(self, headlights=None):
        super().__init__(category='headlight')
        self._headlights = headlights
        self.pin_active = False

    @property
    def last_action(self):
        return self._last_action

    @last_action.setter
    def last_action(self, action):
        if action == 'power_on':
            self.pin_active = True
        elif action == 'power_off':
            self.pin_active = False

        self._last_action = action

    def __str__(self):
        oscillator = str(self._buzzer.oscillator \
                        if self._buzzer is not None \
                        else None)
        return (f'HeadlightState(pin_active={self.pin_active}, '
                f'oscillator={oscillator})')

    def __iter__(self):
        return iter({
            'category': self.category,
            'pinActive': self.pin_active,
            'oscillator': dict(self._headlights.oscillator) \
                            if self._headlights is not None \
                            and self._headlights.oscillator is not None \
                            else None
        }.items())

class IndicatorState(State):
    def __init__(self, indicator=None):
        super().__init__(category='indicator')
        self._indicator = indicator
        self.pins_active = (False, False, False)

    @property
    def last_action(self):
        return self._last_action

    @last_action.setter
    def last_action(self, action):
        if action == 'power_on':
            self.pins_active = (True, True, True)
        elif action == 'power_off':
            self.pins_active = (False, False, False)

        self._last_action = action

    def __str__(self):
        oscillators = str(list(accumulate(dict(self._indicator.oscillators))) \
                        if self._indicator is not None \
                        else None)
        return (f'IndicatorState(pins_active={str(self.pins_active)}, '
                f'oscillators={oscillators})')

    def __iter__(self):
        return iter({
            'category': self.category,
            'pinsActive': self.pins_active,
            'oscillators': list(accumulate(dict(self._indicator.oscillators)))
                            if self._indicator is not None \
                            and self._indicator.oscillators is not None \
                            else None
        }.items())
