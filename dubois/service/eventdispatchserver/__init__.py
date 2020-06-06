import websockets, asyncio, json
from threading import Thread
from dubois import Headlights, Wheels
from ._events import WheelEvent, HeadlightEvent, EventDispatchFailedError
from ._states import HeadlightState
import _logging as logging

logger = logging.getLogger(__name__)
ADDRESS = '0.0.0.0'
PORT = 4201

_headlights = Headlights()
_wheels = Wheels()

class RawEvent:
    def __init__(self, rawData):
        event = json.loads(rawData)
        self.action = event['action']
        self.category = event['category']
        self.params = event['params']

    def __str__(self):
        return {
            'action': self.action,
            'category': self.category,
            'params': self.params
        }

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
                            f'{rawEvent.action}')

            try:
                if rawEvent.category == 'ping':
                    logger.debug('Ping received!')
                elif rawEvent.category == 'wheel':
                    WheelEvent(rawEvent, _wheels).dispatch()
                elif rawEvent.category == 'headlight':
                    HeadlightEvent(rawEvent, _headlights).dispatch()
                    await websocket.send(str(HeadlightState(rawEvent.action, _headlights)))
                else:
                    raise EventDispatchFailedError(f'Unknown event category: {rawEvent.category}')
            except EventDispatchFailedError as e:
                logger.warning(repr(e))
                await websocket.send(str(e))

def start():
    EventDispatchServerThread().start()
    logger.info('Event dispatch server started.')
