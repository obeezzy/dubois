import websockets, asyncio, json
from threading import Thread
import _logging as logging
from ._events import RawEvent, WheelEvent

logger = logging.getLogger(__name__)
PORT = 4201

async def dispatch_event(websocket, path):
    while True:
        event = RawEvent(await websocket.recv())
        logger.debug('Received from (%s): %s' \
                    % (str(websocket.remote_address), event.action))

        if event.type == 'pingEvent':
            logger.debug('Ping received!')
        elif event.type == 'wheelEvent':
            WheelEvent(event).dispatch()

def start():
    start_server = websockets.serve(dispatch_event, '0.0.0.0', PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    webSocketServerThread = Thread(target=asyncio.get_event_loop().run_forever)
    webSocketServerThread.start()
    logger.info("Event dispatch server started.")
