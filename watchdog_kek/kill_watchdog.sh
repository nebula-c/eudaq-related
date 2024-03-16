#!/bin/bash

pid=$(pgrep -f "watchdog_v2.py")
kill -9 $pid
echo "Done"
