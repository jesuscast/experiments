import sqlite3

def obtainRows():
  conn = sqlite3.connect('/var/containers/Shared/SystemGroup/3FE456F0-0DC5-4624-A13B-04D65FCDF2B8/Library/BatteryLife/CurrentPowerlog.PLSQL')
  cur = conn.cursor()
  cur.execute("SELECT '_rowid_',* FROM 'PLBatteryAgent_EventBackward_Battery'  ORDER BY '_rowid_' ASC;")
  rows = cur.fetchall()
  return rows