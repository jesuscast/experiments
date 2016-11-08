from akima import interpolate

def extract_fields(fileName):
  rawFile = open(fileName)
  raw = rawFile.read()
  rawFile.close()

  listData = [ n.split("|") for n in raw.split("\n") ][:-1]
  amperages = [ float(n[8]) for n in listData ]
  timestamps = [ float(n[2]) for n in listData ]
  return amperages, timestamps

def findContainingRange(bigArray, smallArray):
  lenBigArray = len(bigArray)
  lenSmallArray = len(smallArray)
  i = iTmp = 0
  j = jTmp = 1
  while (smallArray[0] > bigArray[i]):
    iTmp = i
    i += 1
    if (i >= lenBigArray):
      return False
  i = iTmp
  while (smallArray[-1] < bigArray[-j]):
    jTmp = j
    j += 1
    if (j == (lenBigArray+1)):
      return False
  j = lenBigArray - jTmp + 1
  return (i, j)

def findInterpolatedPowerValues(timestamps, fileName):
  amperages, timestampsPower = extract_fields(fileName)
  i,j = findContainingRange(timestampsPower, timestamps)
  return interpolate(timestampsPower[i:j], amperages[i:j], timestamps)