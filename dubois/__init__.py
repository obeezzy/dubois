from .dubois_impl.transducers.output import Headlights, Indicator, Wheels
import atexit

@atexit.register
def cleanup():
    import RPi.GPIO as GPIO
    GPIO.cleanup()

    from dubois.oscillators import OscillatorClient
    OscillatorClient().unregister_all()
