#!/usr/bin/python3
import _eventdispatchserver
import _webserver

if __name__ == '__main__':
    _eventdispatchserver.start()
    _webserver.start()
