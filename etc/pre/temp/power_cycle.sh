#!/bin/bash

path1='/dev/hmp4040_2'

HAMEG -p $path1 --off
sleep 1
HAMEG -p $path1 --on
