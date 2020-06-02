#!/usr/bin/python3
import _eventdispatchserver
import _oscillatorserver
import _webserver
import RPi.GPIO as GPIO
import atexit

def _shutdown():
    GPIO.cleanup()

if __name__ == '__main__':
    _eventdispatchserver.start()
    _oscillatorserver.start()
    _webserver.start()
    atexit.register(_shutdown)
