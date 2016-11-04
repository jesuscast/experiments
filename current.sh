#!/bin/bash

ssh root@192.168.1.153 dump
scp root@192.168.1.153:/tmp/data_dump.* $(pwd)/latest/