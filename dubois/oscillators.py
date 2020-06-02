import websockets, asyncio, json
from threading import Thread
from abc import ABC, abstractmethod
from . import _logging as logging

logger = logging.getLogger(__name__)
ADDRESS = '127.0.0.1'
PORT = 4202

class OscillatorRule:
    def __init__(self, *, pins, recipe):
        self.action = ''
        self.pins = pins
        self.recipe = recipe

    def __str__(self):
        return json.dumps({
                'action': self.action,
                'pins': self.pins,
                'recipe': self.recipe,
            })

class OscillatorClient:
    def __init__(self, *, serverAddress=ADDRESS, serverPort=PORT):
        self.uri = f'ws://{serverAddress}:{serverPort}'

    def register(self, rule):
        rule.action = 'add'
        asyncio.get_event_loop().run_until_complete(self._post(rule))

    def unregister(self, rule):
        rule.action = 'remove'
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

class Blink(Oscillator):
    def __init__(self, *, onTime=500, offTime=500):
        super().__init__()
        self.onTime = onTime
        self.offTime = offTime
    def recipe(self):
        return f'T {self.onTime} T {self.offTime}'
