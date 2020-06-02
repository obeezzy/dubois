import websockets, asyncio, json, time
import RPi.GPIO as GPIO
from threading import Thread
import _logging as logging

logger = logging.getLogger(__name__)
ADDRESS = '127.0.0.1'
PORT = 4202

_pinOscillators = []

class OscillatorRule:
    def __init__(self, rawData):
        rule = json.loads(rawData)
        self.action = rule['action']
        self.pins = rule['pins']
        self.recipe = rule['recipe']

    def __str__(self):
        return (f'OscillatorRule(action={self.action}, '
                f'pins={", ".join(str(p) for p in self.pins)}, '
                f'recipe={self.recipe})')

class PinOscillator(Thread):
    def __init__(self, *, pin, rule):
        super().__init__()
        self.pin = pin
        self.rule = rule
        self._stopRequested = False

    def oscillate(self, *, rule=None):
        if rule is not None:
            self.rule = rule
        self.start()
        logger.debug(f'PinOscillator started for {self.pin}.')

    def stop(self):
        logger.debug(f'PinOscillator invoked stop() for {self.pin}.')
        self._stopRequested = True
        self.join()
        logger.debug(f'PinOscillator stopped() for {self.pin}.')

    def run(self):
        logger.debug(f'PinOscillator({self.pin}) started.')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)

        recipeSymbols = self.rule.recipe.split(' ')
        pinActive = False
        while not self._stopRequested:
            for symbol in recipeSymbols:
                if self._stopRequested:
                    break
                elif symbol.upper() == 'T':
                    pinActive = not pinActive
                    GPIO.output(self.pin, pinActive)
                elif symbol.isdigit():
                    time.sleep(int(symbol) / 1000)
                else:
                    logger.warning(f'Unknown symbol: {symbol}')

        GPIO.output(self.pin, GPIO.LOW)
        GPIO.cleanup()
        logger.debug(f'PinOscillator({self.pin}) terminated.')

class OscillatorServerThread(Thread):
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
                                            _pinOscillators)
            pinsToAdd = list(rule.pins)

            for osc in oscillatorsToUpdate:
                osc.stop()
                osc.oscillate(rule=rule)
                pinsToAdd.remove(osc.pin)
            for pin in pinsToAdd:
                osc = PinOscillator(pin=pin, rule=rule)
                osc.oscillate()
                _pinOscillators.append(osc)
        elif rule.action == 'remove':
            oscillatorsToRemove = filter(lambda osc: True if osc.pin in rule.pins else False,
                                            _pinOscillators)
            for osc in oscillatorsToRemove:
                osc.stop()
                _pinOscillators.remove(osc)
        else:
            logger.warning('Unhandled oscillator rule.')

def start():
    OscillatorServerThread().start()
    logger.info('Oscillator server started.')
