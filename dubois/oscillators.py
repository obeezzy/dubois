import websockets, asyncio, json
from threading import Thread
from abc import ABC, abstractmethod

ADDRESS = '127.0.0.1'
PORT = 4202

class OscillatorRule:
    def __init__(self, *, pins, recipe, action='', timestamp=None):
        self.pins = pins
        self.recipe = recipe
        self.action = action
        self.timestamp = timestamp

    def __str__(self):
        return json.dumps({
                'action': self.action,
                'pins': self.pins,
                'recipe': self.recipe,
                'timestamp': self.timestamp \
                                if self.timestamp is not None \
                                else 0,
            })

class OscillatorClient:
    def __init__(self, *, server_address=ADDRESS, server_port=PORT):
        self.uri = f'ws://{server_address}:{server_port}'

    def register(self, rule):
        rule.action = 'add'
        asyncio.get_event_loop().run_until_complete(self._post(rule))

    def unregister(self, rule):
        rule.action = 'remove'
        asyncio.get_event_loop().run_until_complete(self._post(rule))

    def unregister_all(self):
        rule = OscillatorRule(action='remove_all', pins=[], recipe='')
        asyncio.get_event_loop().run_until_complete(self._post(rule))

    async def _post(self, rule):
        async with websockets.connect(self.uri) as websocket:
            await websocket.send(str(rule))

class Oscillator(ABC):
    def __init__(self):
        self._client = OscillatorClient()

    @property
    @abstractmethod
    def recipe(self):
        pass

    def start(self, *, pins, timestamp=None):
        if not isinstance(pins, list):
            raise ValueError('"pins" argument must be of type "list".')
        self.rule = OscillatorRule(pins=pins,
                                    recipe=self.recipe(),
                                    timestamp=timestamp)
        self._client.register(self.rule)

    def stop(self):
        if hasattr(self, 'rule') and self.rule is not None:
            self._client.unregister(self.rule)

class Flash(Oscillator):
    def __init__(self, *, on_time=500, off_time=500):
        super().__init__()
        self.on_time = on_time
        self.off_time = off_time
    def recipe(self):
        return (f'T {self.on_time} '
                f'T {self.off_time}')

class DoubleFlash(Oscillator):
    def __init__(self, *, burst_time=50, off_time=500):
        super().__init__()
        self.burst_time = burst_time
        self.off_time = off_time
    def recipe(self):
        return (f'T {self.burst_time} '
                f'T {self.burst_time} '
                f'T {self.burst_time} '
                f'T {self.off_time}')

class TripleFlash(Oscillator):
    def __init__(self, *, burst_time=50, off_time=500):
        super().__init__()
        self.burst_time = burst_time
        self.off_time = off_time
    def recipe(self):
        return (f'T {self.burst_time} '
                f'T {self.burst_time} '
                f'T {self.burst_time} '
                f'T {self.burst_time} '
                f'T {self.burst_time} '
                f'T {self.off_time}')

class AlwaysOn(Oscillator):
    def __init__(self):
        super().__init__()
    def recipe(self):
        return 'T'

class AlwaysOff(Oscillator):
    def __init__(self):
        super().__init__()
    def recipe(self):
        return ''

class Inline(Oscillator):
    def __init__(self, recipe):
        super().__init__()
        self._recipe = recipe
    def recipe(self):
        return self._recipe
