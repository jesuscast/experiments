from ctypes import Structure, c_double
from objc_util import *
import time
from akima import interpolate
import numpy as np
from dtensor import dtensor
from ktensor import ktensor
from cp import als
import requests

class PointStruct:
  """ Parser for objective c sensor struct.
    Saves x,y,z for sensor as well as t for
    the time
  """
  def __init__(self, data):
    points = None
    if self.name == 'CMRotationRate':
      points = data.rotationRate(argtypes=[])
    elif self.name == 'CMAcceleration':
      points = data.acceleration(argtypes=[])
    elif self.name == 'CMMagneticField':
      points = data.magneticField(argtypes = [])
    else:
      raise Exception('Error. type not supported')
    self.x = points.a
    self.y = points.b
    self.z = points.c
    self.p = (self.x, self.y, self.z)
    self.t = data.timestamp(argtypes=[])

class CMRotationRate(PointStruct):
  name = 'CMRotationRate'

class CMAcceleration(PointStruct):
  name = 'CMAcceleration'

class CMMagneticField(PointStruct):
  name = 'CMMagneticField'

# The number of readings per second.
necessary = 50
# the CMotionManager instance
mgr = None

# Initialize the objects.
CMMotionManager = ObjCClass('CMMotionManager')
mgr = CMMotionManager.alloc().init()
# Start receiving data.
mgr.startGyroUpdates()
mgr.startAccelerometerUpdates()
mgr.startMagnetometerUpdates()

def collectForNTime(miliseconds):
  """ Returns readings and timestamps for up to N miliseconds """
  gyroData = None
  accelData = None
  magneticData = None
  timesP = [0,0,0]
  readings = [[],[],[]]
  timesFinal = [[],[],[]]
  timeA = time.time()
  while True:
    timeB = time.time()
    if(timeB - timeA) >= miliseconds:
      break
    gyroData = mgr.gyroData()
    accelData = mgr.accelerometerData()
    magneticData = mgr.magnetometerData()
    if gyroData and accelData and magneticData:
      gyroData = CMRotationRate(gyroData)
      accelData = CMAcceleration(accelData)
      magneticData = CMMagneticField(magneticData)
      for i, sensorItem in enumerate([ gyroData, accelData, magneticData]):
        if sensorItem.t != timesP[i]:
          timesP[i] = sensorItem.t
          timesFinal[i].append(sensorItem.t)
          readings[i].append(list(sensorItem.p))
  return readings, timesFinal

def normalizeReadings(readings, timestampsTmp):
  """ Interpolate all of the readings in order to obtain N number of readings per second """
  readingsNormalizedTmp = []

  earliestTimestamp = np.amax([ n[0] for n in timestampsTmp ])+0.0001
  latestTimestamp = np.amin([ n[-1] for n in timestampsTmp ])-0.0001

  newXValues = np.arange(earliestTimestamp, latestTimestamp, (latestTimestamp - earliestTimestamp) / float(necessary))

  for i in range(len(readings)):
    for k in range(3):
      currentColumnSensor = []
      timestamps = []
      for j in range(len(readings[i])):
        timestamps.append(timestampsTmp[i][j])
        currentColumnSensor.append(readings[i][j][k])
      # print(str(timestamps[0])+','+str(timestamps[-1]))
      # print(str(newXValues[0])+','+str(newXValues[-1]))
      currentColumnInterpolated = interpolate(timestamps, currentColumnSensor, newXValues)
      readingsNormalizedTmp.append(currentColumnInterpolated)

  return readingsNormalizedTmp, newXValues

def obtainCompressedCSV(readingsNormalized):
  """ Compresses teh sensor data """
  T_in= dtensor(readingsNormalized.reshape(necessary,3,3))
  T_out, fit, itr, _ = als(T_in, 3)
  final_Compressed = "\n".join(
    [ ",".join([ str(k) for k in n ]) for n in T_out.U[0]  ] +
    [ ",".join([ str(k) for k in n ]) for n in T_out.U[1]  ] +
    [ ",".join([ str(k) for k in n ]) for n in T_out.U[2]  ] +
    [ ",".join([ str(n) for n in T_out.lmbda ])]
  )
  return final_Compressed

def obtainCSV(readingsNormalized):
  """ Creates a CSV out of the normalized matrix """
  final_Uncompressed = "\n".join([  ",".join([ str(readingsNormalized[i][j]) for j in range(9) ]) for i in range(necessary) ])
  return final_Uncompressed

def toNormal(readings, timestamps):
  """ Normalize the data and puts the matrix
    in the right format for
   tensor compression """
  data = normalizeReadings(readings, timestamps)
  times = data[1][:necessary]
  organizedSensor = np.array([  [ data[0][j][i] for j in range(9) ] for i in range(necessary) ])
  return organizedSensor, times

def  startColecting(serverIP):
  """Start collecting the data """
  print('*'*10)
  print("Initial time:"+str(time.time()))
  timesDiff = []
  allTimes = []
  for i in range(180):
    fileToWrite = open('current_data.csv', 'w')
    results = []
    for j in range(20):
      data, times = toNormal(*collectForNTime(1))
      timeInitial = time.time()
      inCSV = obtainCompressedCSV(data)
      timesDiff.append(time.time() - timeInitial)
      allTimes.append(times)
      results.append(inCSV)
    fileToWrite.write(("*"*100).join(results))
    fileToWrite.close()
    files = { 'file': open('current_data.csv', 'rb') }
    data = {
      'fieldType': 'compressed',
    }
    r = requests.post('http://'+serverIP+'/csv/upload', files = files, data = data)
    print(i)
  print('Final time: '+str(time.time()))
  return timesDiff, allTimes

# a,b = startColecting()
# 192.168.1.15