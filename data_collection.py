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

necessary = 50
mgr = None

CMMotionManager = ObjCClass('CMMotionManager')
mgr = CMMotionManager.alloc().init()
mgr.startGyroUpdates()
mgr.startAccelerometerUpdates()
mgr.startMagnetometerUpdates()

def collectForNTime(miliseconds):
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
      for sensorItem in enumerate([ gyroData, accelData, magneticData]):
        if sensorItem.t != timesP[i]:
          timesP[i] = sensorItem.t
          timesFinal[i].append(sensorItem.t)
          readings[i].append(list(sensorItem.p))
  return readings, timesFinal

def normalizeReadings(readings, timestampsTmp):

  readingsNormalizedTmp = []

  earliestTimestamp = np.amax([ n[0] for n in timestampsTmp ])
  latestTimestamp = np.amin([ n[-1] for n in timestampsTmp ])

  newXValues = np.arange(earliestTimestamp, latestTimestamp, (latestTimestamp - earliestTimestamp) / float(necessary))

  for i in range(len(readings)):
    currentColumnSensor = []
    timestamps = []
    for j in range(len(readings[i])):
      timestamps.append(timestampsTmp[i][j])
      currentColumnSensor.append(readings[i][j])
    currentColumnInterpolated = interpolate(timestamps, currentColumnSensor, newXValues)
    readingsNormalizedTmp.append(currentColumnInterpolated)

  return readingsNormalizedTmp, newXValues

def obtainCompressedCSV(readingsNormalized):
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
  final_Uncompressed = "\n".join([  ",".join([ str(readingsNormalized[i][j]) for j in range(9) ]) for i in range(necessary) ])
  return final_Uncompressed

def toNormal(readings, timestamps):
  data = normalizeReadings(readings, timestamps)
  times = data[1][:necessary]
  organizedSensor = np.array([  [ data[0][j][i] for j in range(9) ] for i in range(necessary) ])
  return organizedSensor, times

# readings, timestamps = collectForNTime(1)
# readingsNormalized = [  [ normalizeReadings(readings)[j][i] for j in range(9) ] for i in range(necessary) ]

def  startColecting():
  print("Initial time:"+str(time.time()))
  for i in range(180):
    fileToWrite = open('current_data.csv', 'w')
    for j in range(20):
      data, times = toNormal(*collectForNTime(1))
      inCSV = obtainCompressedCSV(data)
      fileToWrite.write(inCSV+'\n')
    fileToWrite.write('*'*100+'\n')
    fileToWrite.close()
    files = { 'file': open('current_data.csv', 'rb') }
    data = {
      'fieldType': 'compressed',
    }
    r = requests.post('http://8f6eea6f.ngrok.io/csv/upload', files = files, data = data)
    print('*'*10)
    print(r)
    print(i)
    print(time.time())

startColecting()