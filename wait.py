import os
import time

def waitcls(sleepTime, speedMode):
    version = os.name

    clearCommand = ''

    match version:
        case 'nt':
            clearCommand = 'cls'
        case 'Posix':
            clearCommand = 'clear'


    if speedMode:
        time.sleep(0)
    else:
        time.sleep(sleepTime)
    os.system(clearCommand)