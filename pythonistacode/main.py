from datacollection import startColecting
from powerlogs import obtainRows
import requests

EXPERIMENT_ID = '1'
SERVER_IP = '192.168.1.15'
CYCLES = 180
CYCLE_LENGTH = 20

timesDiff, allTimes, initialTime, finalTime = startColecting(SERVER_IP, CYCLES, CYCLE_LENGTH, EXPERIMENT_ID)

# r = requests.post('http://'+SERVER_IP+'/csv/upload', files = files, data = data)

# a,b = startColecting()
# 192.168.1.15