import os
from wowlib import log



logname = os.path.splitext(__file__)[0]
#print(logname)


@log.log(logname)
def test():
    print('hello')


test()