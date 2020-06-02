from .dubois_impl.transducers.output import Headlights, Indicator, Wheels
from .dubois_impl.oscillators import Flash, AlwaysOn, AlwaysOff
import atexit

@atexit.register
def cleanup():
    import RPi.GPIO as GPIO
    GPIO.cleanup()

    from .dubois_impl.oscillators import OscillatorClient
    OscillatorClient().unregister_all()
