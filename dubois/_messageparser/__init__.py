import websockets, asyncio
from transducers.output import Wheels
from threading import Thread
import _logging as logging

logger = logging.getLogger(__name__)

wheels = Wheels()
PORT = 4201

class Message:
    def __init__(self, rawData):
        message = json.loads(receivedData)
        self.action = message.action
        self.params = message.params

async def parse_message(websocket, path):
    logger.debug("Path: %s" % path)
    message = Message(await websocket.recv())
    if message.params['activated']:
        if message.action == 'move_forward':
            wheels.move_forward()
        elif message.action == 'move_backward':
            wheels.move_backward()
        elif message.action == 'move_clockwise':
            wheels.move_clockwise()
        elif message.action == 'move_counterclockwise':
            wheels.move_counterclockwise()
    else:
        wheels.stop()

def start():
    start_server = websockets.serve(parse_message, '0.0.0.0', PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    webSocketServerThread = Thread(target=asyncio.get_event_loop().run_forever)
    webSocketServerThread.start()
    logger.info("Message parser server started.")

