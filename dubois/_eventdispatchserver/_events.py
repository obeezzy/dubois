import _logging as logging
from transducers.output import Wheels

logger = logging.getLogger(__name__)
_wheels = Wheels()

class Event(object):
    def dispatch(self):
        pass

class WheelEvent(Event):
    def __init__(self, rawEvent):
        self.action = rawEvent.action
        self.timeout = rawEvent.params.get('timeout', 200)

    def dispatch(self):
        if self.action == 'move_forward':
            _wheels.move_forward(timeout=self.timeout)
        elif self.action == 'move_backward':
            _wheels.move_backward(timeout=self.timeout)
        elif self.action == 'move_clockwise':
            _wheels.move_clockwise(timeout=self.timeout)
        elif self.action == 'move_counterclockwise':
            _wheels.move_counterclockwise(timeout=self.timeout)
        _wheels.stop()

    def __str__(self):
        return (f'WheelEvent(action={self.action}, '
                f'timeout={self.timeout})')
