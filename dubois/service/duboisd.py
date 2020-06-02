#!/usr/bin/python3
import eventdispatchserver, oscillatorserver, webserver
import atexit
import RPi.GPIO as GPIO

def _shutdown():
    GPIO.cleanup()

if __name__ == '__main__':
    eventdispatchserver.start()
    oscillatorserver.start()
    webserver.start()
    atexit.register(_shutdown)
