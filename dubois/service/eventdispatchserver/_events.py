from abc import ABC, abstractmethod
import _logging as logging

logger = logging.getLogger(__name__)

class Event(ABC):
    @abstractmethod
    def dispatch(self):
        pass

class EventDispatchFailedError(RuntimeError):
    def __init__(self, message):
        self.category = 'error'
        self.message = message

    def __str__(self):
        return f'EventDispatchFailedError(message={self.message})'

    def __iter__(self):
        return iter({
            'category': self.category,
            'message': self.message,
        }.items())

class BuzzerEvent(Event):
    def __init__(self, rawEvent, buzzer):
        self.action = rawEvent.action
        self._buzzer = buzzer

    def dispatch(self):
        if self.action == 'power_on':
            self._buzzer.power_on()
        elif self.action == 'power_off':
            self._buzzer.power_off()
        else:
            raise EventDispatchFailedError(f'Unhandled action: {self.action}')

    def __str__(self):
        return f'BuzzerEvent(action={self.action})'

class HeadlightEvent(Event):
    def __init__(self, rawEvent, headlights):
        self.action = rawEvent.action
        self._headlights = headlights

    def dispatch(self):
        if self.action == 'power_on':
            self._headlights.power_on()
        elif self.action == 'power_off':
            self._headlights.power_off()
        else:
            raise EventDispatchFailedError(f'Unhandled action: {self.action}')

    def __str__(self):
        return f'HeadlightEvent(action={self.action})'

class IndicatorEvent(Event):
    def __init__(self, rawEvent, indicator):
        self.action = rawEvent.action
        self._indicator = indicator

    def dispatch(self):
        if self.action == 'power_on':
            self._indicator.power_on()
        elif self.action == 'power_off':
            self._indicator.power_off()
        else:
            raise EventDispatchFailedError(f'Unhandled action: {self.action}')

    def __str__(self):
        return f'IndicatorEvent(action={self.action})'

class WheelEvent(Event):
    def __init__(self, rawEvent, wheels):
        self.action = rawEvent.action
        self.timeout = rawEvent.params.get('timeout', 200)
        self._wheels = wheels

    def dispatch(self):
        if self.action == 'move_forward':
            self._wheels.move_forward(timeout=self.timeout)
        elif self.action == 'move_backward':
            self._wheels.move_backward(timeout=self.timeout)
        elif self.action == 'move_clockwise':
            self._wheels.move_clockwise(timeout=self.timeout)
        elif self.action == 'move_counterclockwise':
            self._wheels.move_counterclockwise(timeout=self.timeout)
        else:
            logger.warning(f'Unhandled action: {self.action}')
        self._wheels.stop()

    def __str__(self):
        return (f'WheelEvent(action={self.action}, '
                f'timeout={self.timeout})')
