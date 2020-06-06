import websockets, asyncio, json
from threading import Thread
from abc import ABC, abstractmethod

ADDRESS = '127.0.0.1'
PORT = 4202

class OscillatorClient:
    def __init__(self, *,
                    server_address=ADDRESS,
                    server_port=PORT):
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
    INFINITE = -1
    def __init__(self, *, loops=INFINITE):
        self._client = OscillatorClient()
        self.loops = loops
        self.rule = None

    @property
    @abstractmethod
    def recipe(self):
        pass

    def start(self, *, pins, timestamp=None):
        if not isinstance(pins, list):
            raise ValueError('"pins" argument must be of type "list".')
        self.rule = OscillatorRule(pins=pins,
                                    recipe=self.recipe(),
                                    loops=self.loops,
                                    timestamp=timestamp)
        self._client.register(self.rule)

    def stop(self):
        if hasattr(self, 'rule') and self.rule is not None:
            self._client.unregister(self.rule)

    def __repr__(self):
        return f'Oscillator(rule={repr(self.rule)}, loops={self.loops})'

    def __str__(self):
        return json.dumps({
            'rule': json.loads(str(self.rule)),
            'loops': self.loops,
        })

class OscillatorRule:
    def __init__(self, *,
                    pins,
                    recipe,
                    action='',
                    loops=Oscillator.INFINITE,
                    timestamp=None):
        self.action = action
        self.loops = loops
        self.pins = pins
        self.recipe = recipe
        self.timestamp = timestamp

    def __repr__(self):
        return (f'OscillatorRule('
                f'action={self.action}, '
                f'loops={self.loops}, '
                f'pins={self.pins}, '
                f'recipe={self.recipe}, '
                f'timestamp={self.timestamp}'
                f')')

    def __str__(self):
        return json.dumps({
                'action': self.action,
                'loops': self.loops,
                'pins': self.pins,
                'recipe': self.recipe,
                'timestamp': self.timestamp \
                                if self.timestamp is not None \
                                else 0,
            })

class InvalidRecipeError(RuntimeError):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class Flash(Oscillator):
    def __init__(self, *,
                    on_time=500,
                    off_time=500,
                    loops=Oscillator.INFINITE):
        super().__init__(loops=loops)
        self.on_time = on_time
        self.off_time = off_time
    def recipe(self):
        return (f'T {self.on_time} '
                f'T {self.off_time}')

class DoubleFlash(Oscillator):
    def __init__(self, *,
                    burst_time=50,
                    off_time=500,
                    loops=Oscillator.INFINITE):
        super().__init__(loops=loops)
        self.burst_time = burst_time
        self.off_time = off_time
    def recipe(self):
        return (f'T {self.burst_time} '
                f'T {self.burst_time} '
                f'T {self.burst_time} '
                f'T {self.off_time}')

class TripleFlash(Oscillator):
    def __init__(self, *,
                    burst_time=50,
                    off_time=500,
                    loops=Oscillator.INFINITE):
        super().__init__(loops=loops)
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
    def __init__(self,
                    *recipe,
                    loops=Oscillator.INFINITE):
        super().__init__(loops=1 \
                            if len(recipe) is 1 and isinstance(recipe[0], int) \
                            else Oscillator.INFINITE)
        if len(recipe) is 1 and isinstance(recipe[0], str):
            self._recipe = recipe
        elif len(recipe) is 1 and isinstance(recipe[0], int):
            self._recipe = f'T {recipe[0]} T'
        elif len(recipe) > 0:
            recipe = recipe[0] \
                    if len(recipe) is 1 \
                        and isinstance(recipe[0], list) \
                    else recipe
            self._recipe = ''
            for symbol in recipe:
                if isinstance(symbol, int):
                    self._recipe += 'T ' + str(symbol)
                else:
                    raise InvalidRecipeError(f'Invalid argument: {symbol}')
    def recipe(self):
        return self._recipe

class Sos(Oscillator):
    def __init__(self, *,
                    dot_time=100,
                    dash_time=200,
                    character_delay=30,
                    repeat_delay=800,
                    loops=1):
        super().__init__(loops=loops)
        self.dot_time = dot_time
        self.dash_time = dash_time
        self.character_delay = character_delay
        self.repeat_delay = repeat_delay
    def recipe(self):
        return (f'T {self.dot_time} T {self.character_delay} '
                f'T {self.dot_time} T {self.character_delay} '
                f'T {self.dot_time} T {self.character_delay} '
                f'T {self.dash_time} T {self.character_delay} '
                f'T {self.dash_time} T {self.character_delay} '
                f'T {self.dash_time} T {self.character_delay} '
                f'T {self.dot_time} T {self.character_delay} '
                f'T {self.dot_time} T {self.character_delay} '
                f'T {self.dot_time} T {self.character_delay} '
                f'T {self.dot_time} T {self.repeat_delay}')

class MorseCode(Oscillator):
    DICT = {
            'A':'.-', 'B':'-...',
            'C':'-.-.', 'D':'-..', 'E':'.',
            'F':'..-.', 'G':'--.', 'H':'....',
            'I':'..', 'J':'.---', 'K':'-.-',
            'L':'.-..', 'M':'--', 'N':'-.',
            'O':'---', 'P':'.--.', 'Q':'--.-',
            'R':'.-.', 'S':'...', 'T':'-',
            'U':'..-', 'V':'...-', 'W':'.--',
            'X':'-..-', 'Y':'-.--', 'Z':'--..',
            '1':'.----', '2':'..---', '3':'...--',
            '4':'....-', '5':'.....', '6':'-....',
            '7':'--...', '8':'---..', '9':'----.',
            '0':'-----', ', ':'--..--', '.':'.-.-.-',
            '?':'..--..', '/':'-..-.', '-':'-....-',
            '(':'-.--.', ')':'-.--.-'
    }
    def __init__(self,
                    message,
                    *,
                    dot_time=100,
                    dash_time=200,
                    character_delay=30,
                    word_delay=60,
                    repeat_delay=800,
                    loops=1):
        super().__init__(loops=loops)
        self._cipher = ''
        self._recipe = ''
        message = message.upper()
        for letter in message:
            if letter != ' ':
                self._cipher += MorseCode.DICT[letter] + ' '
            else:
                self._cipher += ' '
        for character in self._cipher:
            if character == '.':
                self._recipe += f'T {dot_time} '
            elif character == '-':
                self._recipe += f'T {dash_time} '
            elif character != ' ':
                raise RuntimeError(f'Invalid Morse code character: {character}')

            if character == ' ':
                self._recipe += f'T {word_delay} '
            else:
                self._recipe += f'T {character_delay} '
        if self._cipher != '':
            self._recipe += f'T {repeat_delay}'

    def recipe(self):
        return self._recipe

class Monostable(Oscillator):
    def __init__(self, *,
                    on_time=3000):
        super().__init__(loops=1)
        self.on_time = on_time
    def recipe(self):
        return f'T {self.on_time} T'
