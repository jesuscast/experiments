#!/bin/bash

cat ./scripts/remote_dump.sh | ssh root@$1
scp root@$1:/tmp/data_dump.* $(pwd)/data/