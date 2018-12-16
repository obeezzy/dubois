import RPi.GPIO as GPIO
import time

print("First program on Raspberri Py. Press CTRL+C to exit.")
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

try:
    while 1:
        GPIO.output(18, GPIO.HIGH)
        time.sleep(.5)
        GPIO.output(18, GPIO.LOW)
        time.sleep(.5)
except KeyboardInterrupt:
    pass
    GPIO.cleanup()
