#!/usr/bin/env python3

import json
import argparse
import os,sys

def readjson():
    with open(args.json,'r',encoding='utf-8') as file:
        jsonconfig = json.load(file)
    return jsonconfig

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trigger board monitoring",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--json',help='Json file to initialize',default="../json_kek/trigger_board.json")
    parser.add_argument('--dt',type=float,help='Time resolution')

    args=parser.parse_args()

    jsonconfig = readjson()
    sw_path = jsonconfig['SW_path']
    monitor = jsonconfig['Monitor']

    cmd = "sudo " + os.path.join(sw_path, monitor) +  " xxxx xxxR xxx1 xxRx xx1x xRxx x1xx Rxxx 1xxx -d 0.01 -n1000 -p /dev/serial/by-id/usb-CERN_ITS3_Trigger_Board_0011-if01-port0"
    if args.dt:
        cmd = "sudo " + os.path.join(sw_path, monitor) +  " xxxx xxxR xxx1 xxRx xx1x xRxx x1xx Rxxx 1xxx -d 0.01 -n1000 -p /dev/serial/by-id/usb-CERN_ITS3_Trigger_Board_0011-if01-port0 --dt {}".format(args.dt)

    os.system(cmd)


