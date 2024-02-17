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
    args=parser.parse_args()

    jsonconfig = readjson()
    sw_path = jsonconfig['SW_path']

    cmd = "sudo " + sw_path + "./readtrgincnts.py xxxx xxxR xxRx xxx1 xx1x xx1R xxR1 xxRR RXXX -d 0.01 -n1000 -p /dev/serial/by-id/usb-CERN_ITS3_Trigger_Board_0011-if01-port0 --dt 1"
    os.system(cmd)


