import websockets, asyncio, json
from threading import Thread
from dubois import Buzzer, Headlights, Indicator, Wheels
from ._events import BuzzerEvent, HeadlightEvent, IndicatorEvent, WheelEvent
from ._events import EventDispatchFailedError
from ._states import BuzzerState, HeadlightState, IndicatorState
import _logging as logging

logger = logging.getLogger(__name__)
ADDRESS = '0.0.0.0'
PORT = 4201

_buzzer = Buzzer()
_headlights = Headlights()
_indicator = Indicator()
_wheels = Wheels()

class RawEvent:
    def __init__(self, rawData):
        event = json.loads(rawData)
        self.action = event['action']
        self.category = event['category']
        self.params = event['params']

    def __str__(self):
        return (f'RawEvent(action={self.action}, '
                f'category={self.category}, '
                f'params={self.params})')

    def __iter__(self):
        return iter({
            'action': self.action,
            'category': self.category,
            'params': self.params
        }.items())

class EventDispatchServerThread(Thread):
    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(self._run, ADDRESS, PORT)
        loop.run_until_complete(start_server)
        loop.run_forever()

    async def _run(self, websocket, path):
        while True:
            rawEvent = RawEvent(await websocket.recv())
            logger.debug(f'Received from ({str(websocket.remote_address)}): ' \
                            f'{str(rawEvent)}')

            try:
                if rawEvent.category == 'buzzer':
                    BuzzerEvent(rawEvent, _buzzer).dispatch()
                    await websocket.send(json.dumps(dict(BuzzerState(rawEvent.action, _buzzer))))
                elif rawEvent.category == 'headlight':
                    HeadlightEvent(rawEvent, _headlights).dispatch()
                    await websocket.send(json.dumps(dict(HeadlightState(rawEvent.action, _headlights))))
                elif rawEvent.category == 'indicator':
                    IndicatorEvent(rawEvent, _indicator).dispatch()
                    await websocket.send(json.dumps(dict(IndicatorState(rawEvent.action, _indicator))))
                elif rawEvent.category == 'wheel':
                    WheelEvent(rawEvent, _wheels).dispatch()
                elif rawEvent.category == 'ping':
                    logger.debug('Ping received!')
                else:
                    raise EventDispatchFailedError(f'Unknown event category: {rawEvent.category}')
            except EventDispatchFailedError as e:
                logger.warning(str(e))
                await websocket.send(json.dumps(dict(e)))

def start():
    EventDispatchServerThread().start()
    logger.info('Event dispatch server started.')
