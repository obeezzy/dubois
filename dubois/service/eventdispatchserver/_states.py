import json
from dubois.oscillators import OscillatorRule
import _logging as logging

logger = logging.getLogger(__name__)

class State(object):
    def __init__(self, category, action):
        self.action = action
        self.category = category

class HeadlightState(State):
    def __init__(self, action, headlights):
        super().__init__('headlight', action)
        self.headlights = headlights
        self.pin_active = False
        if action == 'power_on':
            self.pin_active = True
        elif action == 'power_off':
            self.pin_active = False

    def __repr__(self):
        return (f'HeadlightState(pin_active={self.pin_active}, '
                f'oscillator={str(self.headlights.oscillator)})')

    def __str__(self):
        return json.dumps({
            'category': self.category,
            'pinActive': self.pin_active,
            'oscillator': str(self.headlights.oscillator.rule) \
                                if self.headlights.oscillator is not None \
                                else None,
        })
