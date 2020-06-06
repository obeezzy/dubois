import websockets, asyncio, json
import RPi.GPIO as GPIO
import threading
import _logging as logging

logger = logging.getLogger(__name__)
ADDRESS = '127.0.0.1'
PORT = 4202

_pin_oscillators = []

class OscillatorRule:
    def __init__(self, rawData):
        rule = json.loads(rawData)
        self.action = rule['action']
        self.loops = rule['loops']
        self.pins = rule['pins']
        self.recipe = rule['recipe']
        self.timestamp = rule['timestamp']

    def __str__(self):
        return (f'OscillatorRule(action={self.action}, '
                f'loops={self.loops}, '
                f'pins={", ".join(str(p) for p in self.pins)}, '
                f'recipe={self.recipe}, ' 
                f'timestamp={self.timestamp})')

class PinOscillator(threading.Thread):
    def __init__(self, *, pin, rule):
        super().__init__()
        self.pin = pin
        self.rule = rule
        self._stop_flag = threading.Event()

    def oscillate(self, *, rule=None):
        if rule is not None:
            self.rule = rule
            print('Recipe: {self.rule}')
        self.start()
        logger.debug(f'PinOscillator started for {self.pin}.')

    def stop(self):
        logger.debug(f'PinOscillator invoked stop() for {self.pin}.')
        self._stop_flag.set()
        logger.debug(f'PinOscillator stopped for {self.pin}.')

    @property
    def stopped(self):
        return self._stop_flag.isSet()

    def _wait(self, timeout):
        self._stop_flag.wait(timeout)

    def run(self):
        logger.debug(f'PinOscillator({self.pin}) started.')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)

        latency = int(time.time()) - self.rule.timestamp \
                    if self.rule.timestamp > 0 \
                    else 0
        recipeSymbols = self.rule.recipe.split(' ')
        pinActive = False
        loops = self.rule.loops
        while True:
            if loops > 0:
                loops -= 1
            elif loops == 0:
                break
            for symbol in recipeSymbols:
                if symbol.upper() == 'T':
                    pinActive = not pinActive
                    GPIO.output(self.pin, pinActive)
                elif symbol.isdigit():
                    delayInMs = int(symbol)
                    if latency >= delayInMs:
                        latency -= delayInMs
                        continue
                    else:
                        delayInMs -= latency
                        latency = 0
                        self._wait(delayInMs / 1000)
                else:
                    logger.warning(f'Unknown symbol: {symbol}')

        GPIO.output(self.pin, GPIO.LOW)
        GPIO.cleanup()
        if self in _pin_oscillators:
            _pin_oscillators.remove(self)
        logger.debug(f'PinOscillator({self.pin}) finished execution.')

class OscillatorServerThread(threading.Thread):
    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(self._run, ADDRESS, PORT)
        loop.run_until_complete(start_server)
        loop.run_forever()

    async def _run(self, websocket, path):
        rule = OscillatorRule(await websocket.recv())
        logger.debug(f'Received from ({str(websocket.remote_address)}): '
                        f'{str(rule)}')

        if rule.action == 'add':
            oscillatorsToUpdate = filter(lambda osc: True if osc.pin in rule.pins else False,
                                            _pin_oscillators)
            pinsToAdd = list(rule.pins)

            for osc in oscillatorsToUpdate:
                osc.stop()
                osc.oscillate(rule=rule)
                pinsToAdd.remove(osc.pin)
            for pin in pinsToAdd:
                osc = PinOscillator(pin=pin, rule=rule)
                osc.oscillate()
                _pin_oscillators.append(osc)
        elif rule.action == 'remove':
            oscillatorsToRemove = filter(lambda osc: True if osc.pin in rule.pins else False,
                                            _pin_oscillators)
            for osc in oscillatorsToRemove:
                osc.stop()
                if osc in _pin_oscillators:
                    _pin_oscillators.remove(osc)
        elif rule.action == 'remove_all':
            for osc in _pin_oscillators:
                osc.stop()
            _pin_oscillators.clear()
        else:
            logger.warning('Unhandled oscillator rule.')

def start():
    OscillatorServerThread().start()
    logger.info('Oscillator server started.')
