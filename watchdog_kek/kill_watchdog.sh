#!/bin/bash

pid=$(pgrep -f "watchdog.py")
kill -9 $pid
echo "Done"
