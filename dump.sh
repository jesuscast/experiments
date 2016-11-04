#!/bin/bash

rm -f /tmp/data_dump.db
rm -f /tmp/data_dump.csv
touch /tmp/data_dump.db
touch /tmp/data_dump.csv
echo "SELECT '_rowid_',* FROM 'PLBatteryAgent_EventBackward_Battery'  ORDER BY '_rowid_' ASC;" > /tmp/data_dump.db
sqlite3 /var/containers/Shared/SystemGroup/3FE456F0-0DC5-4624-A13B-04D65FCDF2B8/Library/BatteryLife/CurrentPowerlog.PLSQL < /tmp/data_dump.db >& /tmp/data_dump.csv
echo 'Done!