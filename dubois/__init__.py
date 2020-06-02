from .dubois_impl.transducers.output import Wheels, Headlights
from .dubois_impl.oscillators import Flash
import atexit

@atexit.register
def cleanup():
    import RPi.GPIO as GPIO
    GPIO.cleanup()

    from .dubois_impl.oscillators import OscillatorClient
    OscillatorClient().unregister_all()
