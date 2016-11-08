from onehour import timesDiff, alltimes, initialtime
from power import findInterpolatedPowerValues
from matplotlib import pyplot
import numpy as np

def obtainTimeArrayFromTimeDiff(initialtime, alltimes):
  newTimes = []
  for i in np.arange(0, len(alltimes), 20):
    newTimes.append(alltimes[i][0] - alltimes[0][0] + initialtime)
  return newTimes


formattedTimes = obtainTimeArrayFromTimeDiff(initialtime, alltimes)
xAxis = [ n-formattedTimes[0] for n in formattedTimes ]
discharge = [ -n for n in findInterpolatedPowerValues(formattedTimes, "./latest/data_dump_1.csv") ]

pyplot.errorbar(xAxis, discharge)
pyplot.xlabel('Time (s)')
pyplot.ylabel('Current Discharge (mA)')
pyplot.show()