#!/usr/bin/python3
import atexit
import RPi.GPIO as GPIO
import eventdispatchserver, oscillatorserver, webserver

@atexit.register
def _shutdown():
    GPIO.cleanup()

if __name__ == '__main__':
    eventdispatchserver.start()
    oscillatorserver.start()
    webserver.start()
