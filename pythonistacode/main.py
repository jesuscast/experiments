from datacollection import startColecting
from powerlogs import obtainRows
import requests

EXPERIMENT_ID = '1'
SERVER_IP = '192.168.1.15'
CYCLES = 1
CYCLE_LENGTH = 10

def createExperiment():
  data = {'experimentID': EXPERIMENT_ID}
  createExperimentRequest = requests.post('http://'+SERVER_IP+'/experiment/create', data = data)
  if (createExperimentRequest.status_code != 200):
    return False
  return True

timesDiff, allTimes, initialTime, finalTime = startColecting(SERVER_IP, CYCLES, CYCLE_LENGTH, EXPERIMENT_ID)

# r = requests.post('http://'+SERVER_IP+'/csv/upload', files = files, data = data)

# a,b = startColecting()
# 192.168.1.15