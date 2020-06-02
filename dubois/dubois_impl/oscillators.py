import websockets, asyncio, json
from threading import Thread
from abc import ABC, abstractmethod

ADDRESS = '127.0.0.1'
PORT = 4202

class OscillatorRule:
    def __init__(self, *, pins, recipe, action=''):
        self.pins = pins
        self.recipe = recipe
        self.action = action

    def __str__(self):
        return json.dumps({
                'action': self.action,
                'pins': self.pins,
                'recipe': self.recipe,
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
        rule = OscillatorRule(pins=[], recipe='', action='remove_all')
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

    def start(self, *, pins):
        if not isinstance(pins, list):
            raise ValueError('"pins" argument must be of type "list".')
        self.rule = OscillatorRule(pins=pins,
                                    recipe=self.recipe())
        self._client.register(self.rule)

    def stop(self):
        if self.rule is None:
            raise ValueError('Rule not set.')

        self._client.unregister(self.rule)

class Flash(Oscillator):
    def __init__(self, *, on_time=500, off_time=500):
        super().__init__()
        self.on_time = on_time
        self.off_time = off_time
    def recipe(self):
        return f'T {self.on_time} T {self.off_time}'
