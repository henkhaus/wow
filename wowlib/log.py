import os
import time
import logging
from functools import wraps

log_location = r'/home/asus/logs'

#new_log = locallogger(logname)

def console(message, logname):
    new_log = locallogger(logname)
    new_log.info(message)
    print (message)


def log(logname):
    new_log = locallogger(logname)
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            #new_log = locallogger(logname)
            start = time.time()
            new_log.info('func: '+ str(func.__name__) +' started')
            result = func(*args, **kwargs)
            end = time.time()
            new_log.info('func: '+ str(func.__name__) +' - '+ str(end-start))
            return result
        return wrapper
    return decorate


def locallogger(logname):
    logger = logging.getLogger(logname)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    handler = logging.FileHandler(os.path.join(log_location, logname + '.log'), 'a')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

