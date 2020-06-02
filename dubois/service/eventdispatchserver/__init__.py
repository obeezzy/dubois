import websockets, asyncio, json
from threading import Thread
import _logging as logging
from ._events import WheelEvent

logger = logging.getLogger(__name__)
ADDRESS = '0.0.0.0'
PORT = 4201

class RawEvent:
    def __init__(self, rawData):
        event = json.loads(rawData)
        self.action = event["action"]
        self.type = event["type"]
        self.params = event["params"]

    def __str__(self):
        return {
            'action': self.action,
            'type': self.type,
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
            event = RawEvent(await websocket.recv())
            logger.debug('Received from (%s): %s' \
                        % (str(websocket.remote_address), event.action))

            if event.type == 'pingEvent':
                logger.debug('Ping received!')
            elif event.type == 'wheelEvent':
                WheelEvent(event).dispatch()

def start():
    EventDispatchServerThread().start()
    logger.info('Event dispatch server started.')
