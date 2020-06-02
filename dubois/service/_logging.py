import os, logging, sys
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter("[%(levelname)s] %(name)s (%(asctime)s): %(message)s",
                                "%m-%d-%Y %I:%M:%S")
LOG_FILE = "/tmp/dubois.log"
LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error" : logging.ERROR,
    "critical": logging.CRITICAL
}

def get_console_handler():
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(FORMATTER)
    return consoleHandler

def get_file_handler():
    if not os.path.exists(os.path.dirname(LOG_FILE)):
        os.makedirs(os.path.dirname(LOG_FILE))
    fileHandler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    fileHandler.setFormatter(FORMATTER)
    return fileHandler

def getLogger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVELS[os.environ.get("LOGLEVEL", "warning").lower()])
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger
