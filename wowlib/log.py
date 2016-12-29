import os
import time
import logging
from functools import wraps
#/todo/ Create manual logger for log errors
log_location = r'/home/asus/logs'


# new_log = locallogger(logname)

def console(message, logname):
    new_log = locallogger(logname)
    new_log.info(message)
    print(message)


def log(logname):
    new_log = locallogger(logname)

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # new_log = locallogger(logname)
            start = time.time()
            new_log.info('func: ' + str(func.__name__) + ' started')
            result = func(*args, **kwargs)
            end = time.time()
            new_log.info('func: ' + str(func.__name__) + ' - ' + str(end - start))
            new_log.info('func: ' + str(result))
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

def logdicts(dict1, dict2 = {}):
    if len(dict2) == 0:
        return dict1
    for key in dict1.keys():
        if key in dict2:
            if type(dict2[key]) == int and type(dict1[key])== int:
                dict2[key]+=dict1[key]
        else:
            pass
    return dict2
